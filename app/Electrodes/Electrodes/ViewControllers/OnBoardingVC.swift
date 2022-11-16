//
//  OnBoardingVC.swift
//  Electrodes
//
//  Created by Nick Varenbut on 11/15/22.
//

import UIKit

class OnBoardingVC: UIViewController {
    @IBOutlet weak var viewFirstName: UIView!
    @IBOutlet weak var viewLastName: UIView!
    @IBOutlet weak var viewWorkStation: UIView!
    @IBOutlet weak var btnContinue: UIButton!
    @IBOutlet weak var txtFirstName: UITextField!
    @IBOutlet weak var txtLastName: UITextField!
    @IBOutlet weak var txtWorkStation: UITextField!
    
    @IBOutlet weak var workPicker: UIPickerView!
    
    private var workStations: [Int] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    override func viewDidLoad() {
        super.viewDidLoad()
        self.setupView()
    }

    func setupView() {
        self.viewFirstName.getRoundedCorner(by: 8)
        self.viewFirstName.getBorder(by: 0.5)
        self.viewLastName.getRoundedCorner(by: 8)
        self.viewLastName.getBorder(by: 0.5)
        self.viewWorkStation.getRoundedCorner(by: 8)
        self.viewWorkStation.getBorder(by: 0.5)
        self.btnContinue.getRoundedCorner(by: 8)
    }
    
    func configurePicter() {
        self.workPicker.delegate = self
        self.workPicker.dataSource = self
        self.workPicker.isHidden = false
    }
    
    @IBAction func workStationPressed(_ sender: Any) {
        self.txtLastName.resignFirstResponder()
        self.txtFirstName.resignFirstResponder()
        self.txtWorkStation.resignFirstResponder()
        self.configurePicter()
        if workPicker.isFirstResponder {
            workPicker.resignFirstResponder()
        }
    }
    
    @IBAction func continuePressed(_ sender: Any) {
        self.performSegue(withIdentifier: "toTestingVC", sender: nil)
    }
}

extension OnBoardingVC: UIPickerViewDelegate, UIPickerViewDataSource {
    func numberOfComponents(in pickerView: UIPickerView) -> Int {
        return 1
    }
    
    func pickerView(_ pickerView: UIPickerView,
                    numberOfRowsInComponent component: Int) -> Int {
        return workStations.count
    }
    
    func pickerView(_ pickerView: UIPickerView,
                    titleForRow row: Int,
                    forComponent component: Int) -> String? {
        return String(self.workStations[row])
    }
    
    func pickerView(_ pickerView: UIPickerView,
                    didSelectRow row: Int,
                    inComponent component: Int) {
        let selectedWork = self.workStations[row]
        self.txtWorkStation.text = String(selectedWork)
        self.workPicker.isHidden = true
    }
}
