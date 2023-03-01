import argparse
import logging

import pyqtgraph as pg
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds
from brainflow.data_filter import DataFilter, FilterTypes, DetrendOperations, NoiseTypes
from pyqtgraph.Qt import QtGui, QtCore, QtWidgets
import numpy as np
from scipy.signal import butter, filtfilt, iirnotch

"""
    Plug in Bluetooth to first (closer to user) USB slot. 
    Switch board on to 'BLE' side. 
    Script adapted from the BrainFlow example 
"""

def filter_data(data, fs=250, notch_f0 = 60, Q = 100):
  nyq = 0.5*fs
  # remove dc offset 
  b,a = butter(2, 1/nyq, 'highpass')
  y = filtfilt(b,a,data)

  b_notch, a_notch = iirnotch(notch_f0, Q, fs)
  y = filtfilt(b_notch, a_notch, y)

  return y

def getMAV(rawEMGSignal):
    """ Thif functions compute the  average of EMG signal Amplitude.::
        
            MAV = 1/N * sum(|xi|) for i = 1 --> N
        
        * Input: 
            * raw EMG Signal as list
        * Output: 
            * Mean Absolute Value    
            
        :param rawEMGSignal: the raw EMG signal
        :type rawEMGSignal: list
        :return: the MAV of the EMG Signal
        :rtype: float
    """
    
    MAV = 1/len(rawEMGSignal) *  np.sum([abs(x) for x in rawEMGSignal])    
    return(MAV)

class Graph:
    def __init__(self, board_shim):
        self.board_id = board_shim.get_board_id()
        self.board_shim = board_shim
        self.exg_channels = BoardShim.get_emg_channels(self.board_id)
        self.sampling_rate = BoardShim.get_sampling_rate(self.board_id)
        self.update_speed_ms = 100 ##(0.05 s = 50)
        self.window_size = 4 ## (showing past 4s data in window)
        self.num_points = self.window_size * self.sampling_rate

        self.app = QtWidgets.QApplication([])
        self.win = pg.GraphicsLayoutWidget(title='Real Time Plot - Mean Absolute Value', size=(800, 600))
        self.win.setBackground('w')
        self._init_timeseries()

        timer = QtCore.QTimer()
        timer.timeout.connect(self.update)
        timer.start(self.update_speed_ms)
        QtWidgets.QApplication.instance().exec_()

    def _init_timeseries(self):
        self.plots = list()
        self.curves = list()
        p = self.win.addPlot(row=0, col=0) 
        p.showAxis('left', True)
        p.setLabel('left', 'Mean Absolute Value (mV)')
        p.setMenuEnabled('left', False)
        p.showAxis('bottom', True)
        p.setMenuEnabled('bottom', False)
        p.setRange(yRange=[0,1000])
        p.setTitle('TimeSeries Plot')
        self.plots.append(p)
        curve = p.plot()
        self.curves.append(curve)
        
        pen = pg.mkPen(color=(255, 0, 0))
        curve_hori = p.plot(pen=pen)
        self.curves.append(curve_hori)

    def update(self):
        data = self.board_shim.get_current_board_data(self.num_points)
        target_channel = self.exg_channels[0]
        target_data = data[target_channel]

        DataFilter.detrend(target_data, DetrendOperations.CONSTANT.value)
        # DataFilter.perform_highpass(target_data, self.sampling_rate, 1/125, 2,
        #                                 FilterTypes.BUTTERWORTH.value, 0)
        # DataFilter.remove_environmental_noise(target_data, self.sampling_rate, NoiseTypes.SIXTY.value)

        target_data = filter_data(target_data)
        
        ## compute metric 
        mavs = []
        mav_window_data_size = 500
        for i in range(len(target_data) - mav_window_data_size + 1):
            mavs.append(getMAV(target_data[i: i + mav_window_data_size]))
        
        print(len(mavs))
        ## save to csv 
        save_data = data[:target_channel, :1] ## write_file takes 2D arrays, here is 1 number 2D array (1,1)
        DataFilter.write_file(save_data, '/Users/jessysong/Documents/Github-Projects/CTS-early-detection/signal-processing/src/stream/sample_data.csv', 'a')  # use 'a' for append mode
        save_mav = np.zeros((1, 1))
        
        if len(mavs)>mav_window_data_size: 
            save_mav.fill(mavs[0])
            DataFilter.write_file(save_mav, '/Users/jessysong/Documents/Github-Projects/CTS-early-detection/signal-processing/src/stream/sample_mav.csv', 'a')  # use 'a' for append mode

            self.curves[0].setData(mavs)
        
        ## set line to hold force at 
        target_mav = [200]*len(mavs)
        self.curves[1].setData(target_mav)
        self.win.show() # you need to add this  
        self.app.processEvents()


def main():
    BoardShim.enable_dev_board_logger()
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser()
    # use docs to check which parameters are required for specific board, e.g. for Cyton - set serial port
    parser.add_argument('--timeout', type=int, help='timeout for device discovery or connection', required=False,
                        default=0)
    parser.add_argument('--ip-port', type=int, help='ip port', required=False, default=0)
    parser.add_argument('--ip-protocol', type=int, help='ip protocol, check IpProtocolType enum', required=False,
                        default=0)
    parser.add_argument('--ip-address', type=str, help='ip address', required=False, default='')
    parser.add_argument('--serial-port', type=str, help='serial port', required=False, default='/dev/cu.usbserial-DM00Q822')
    parser.add_argument('--mac-address', type=str, help='mac address', required=False, default='')
    parser.add_argument('--other-info', type=str, help='other info', required=False, default='')
    parser.add_argument('--serial-number', type=str, help='serial number', required=False, default='')
    parser.add_argument('--board-id', type=int, help='board id, check docs to get a list of supported boards',
                        required=False, default=BoardIds.CYTON_BOARD)
    parser.add_argument('--file', type=str, help='file', required=False, default='')
    parser.add_argument('--streamer-params', type=str, help='streamer params', required=False, default='')
    parser.add_argument('--master-board', type=int, help='master board id for streaming and playback boards',
                        required=False, default=BoardIds.NO_BOARD)
    args = parser.parse_args()

    params = BrainFlowInputParams()
    params.ip_port = args.ip_port
    params.serial_port = args.serial_port
    params.mac_address = args.mac_address
    params.other_info = args.other_info
    params.serial_number = args.serial_number
    params.ip_address = args.ip_address
    params.ip_protocol = args.ip_protocol
    params.timeout = args.timeout
    params.file = args.file
    params.master_board = args.master_board

    try:
        board_shim = BoardShim(args.board_id, params)
        board_shim.prepare_session()
        board_shim.start_stream(450000, args.streamer_params)

        ## Try dummy board - only 1 data point or sth 
        # params = BrainFlowInputParams()
        # board_shim = BoardShim(BoardIds.SYNTHETIC_BOARD, params)
        # board_shim.prepare_session()
        Graph(board_shim)
    except BaseException:
        logging.warning('Exception', exc_info=True)
    finally:
        logging.info('End')
        if board_shim.is_prepared():
            logging.info('Releasing session')
            board_shim.release_session()

if __name__ == '__main__':
    main()