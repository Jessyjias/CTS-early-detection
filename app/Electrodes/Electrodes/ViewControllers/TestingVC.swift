//
//  TestingVC.swift
//  Electrodes
//
//  Created by Nick Varenbut on 11/15/22.
//

import UIKit

class TestingVC: UIViewController {
    @IBOutlet weak var viewOne: UIView!
    @IBOutlet weak var viewTwo: UIView!
    @IBOutlet weak var viewThree: UIView!
    @IBOutlet weak var viewFour: UIView!
    @IBOutlet weak var viewFive: UIView!
    
    @IBOutlet weak var lblOne: UILabel!
    @IBOutlet weak var lblTwo: UILabel!
    @IBOutlet weak var lblThree: UILabel!
    @IBOutlet weak var lblFour: UILabel!
    @IBOutlet weak var lblFive: UILabel!
    
    @IBOutlet weak var viewPlaceholderOne: UIView!
    @IBOutlet weak var viewPlaceholderTwo: UIView!
    
    @IBOutlet weak var lblStep: UILabel!
    @IBOutlet weak var lblDescription: UILabel!
    @IBOutlet weak var btnNext: UIButton!
    
    private var selectedStep: Int = 0
    
    override func viewDidLoad() {
        super.viewDidLoad()
        self.viewOne.getRoundedCorner(by: self.viewOne.frame.height/2)
        self.viewTwo.getRoundedCorner(by: self.viewOne.frame.height/2)
        self.viewThree.getRoundedCorner(by: self.viewOne.frame.height/2)
        self.viewFour.getRoundedCorner(by: self.viewOne.frame.height/2)
        self.viewFive.getRoundedCorner(by: self.viewOne.frame.height/2)
        
        self.viewOne.getBorder(by: 0.5)
        self.viewTwo.getBorder(by: 0.5)
        self.viewThree.getBorder(by: 0.5)
        self.viewFour.getBorder(by: 0.5)
        self.viewFive.getBorder(by: 0.5)
        
        self.viewPlaceholderOne.getRoundedCorner(by: 8)
        self.viewPlaceholderTwo.getRoundedCorner(by: 8)
        self.btnNext.getRoundedCorner(by: 8)
        
        self.performSelection()
    }
    
    @IBAction func nextPressed(_ sender: Any) {
        if self.selectedStep <= 4 {
            self.selectedStep += 1
            self.performSelection()
        }
    }
    
    
    func performSelection() {
        switch self.selectedStep {
        case 0:
            print("selected 1")
            self.viewOne.backgroundColor = .systemGray3
            self.viewTwo.backgroundColor = .white
            self.viewThree.backgroundColor = .white
            self.viewFour.backgroundColor = .white
            self.viewFive.backgroundColor = .white
            self.btnNext.setTitle("Next", for: .normal)
        case 1:
            print("selected 2")
            self.viewOne.backgroundColor = .white
            self.performAnimation(view: self.viewTwo)
            self.viewThree.backgroundColor = .white
            self.viewFour.backgroundColor = .white
            self.viewFive.backgroundColor = .white
            self.lblStep.text = "Step 2"
            self.lblDescription.text = "Put all the electrodes and place them on your hand, as shown below."
            self.btnNext.setTitle("Next", for: .normal)
        case 2:
            print("selected 3")
            self.viewOne.backgroundColor = .white
            self.viewTwo.backgroundColor = .white
            self.performAnimation(view: self.viewThree)
            self.viewFour.backgroundColor = .white
            self.viewFive.backgroundColor = .white
            self.lblStep.text = "Step 3"
            self.lblDescription.text = "Press the button to apply force. Keep pushing the button until the bar is filled."
            self.btnNext.setTitle("Next", for: .normal)
        case 3:
            print("selected 4")
            self.viewOne.backgroundColor = .white
            self.viewTwo.backgroundColor = .white
            self.viewThree.backgroundColor = .white
            self.performAnimation(view: self.viewFour)
            self.viewFive.backgroundColor = .white
            self.lblStep.text = "Step 4"
            self.lblDescription.text = "Analysing..."
            self.btnNext.setTitle("Next", for: .normal)
        case 4:
            print("selected 5")
            self.viewOne.backgroundColor = .white
            self.viewTwo.backgroundColor = .white
            self.viewThree.backgroundColor = .white
            self.viewFour.backgroundColor = .white
            self.performAnimation(view: self.viewFive)
            self.viewPlaceholderOne.isHidden = false
            self.viewPlaceholderTwo.isHidden = false
            self.lblStep.text = "Step 5"
            self.lblDescription.text = "Your result for CTS are as follows:"
            self.btnNext.setTitle("Finish", for: .normal)
        default:
            break
        }
    }
    
    func performAnimation(view: UIView) {
        UIView.animate(withDuration: 0.6) {
            view.backgroundColor = .systemGray3
        }
    }
}
