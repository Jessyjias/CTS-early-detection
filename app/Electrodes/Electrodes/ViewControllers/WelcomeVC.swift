//
//  WelcomeVC.swift
//  Electrodes
//
//  Created by Nick Varenbut on 11/15/22.
//

import UIKit

class WelcomeVC: UIViewController {
    @IBOutlet weak var workIdTextFIeldParentView: UIView!
    @IBOutlet weak var continueButton: UIButton!
    @IBOutlet weak var workIdTextField: UITextField!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        self.navigationController?.navigationBar.isHidden = true
        self.setupView()
    }

    func setupView() {
        self.workIdTextFIeldParentView.getRoundedCorner(by: 8)
        self.workIdTextFIeldParentView.getBorder(by: 0.5)
        self.continueButton.getRoundedCorner(by: 8)
        workIdTextField.delegate = self
    }
    
    @IBAction func continuePressed(_ sender: Any) {
        self.performSegue(withIdentifier: "toOnBoardingVC", sender: nil)
    }
}

extension WelcomeVC: UITextFieldDelegate {
    func textFieldShouldReturn(_ textField: UITextField) -> Bool {
        workIdTextField.resignFirstResponder()
        return true
    }
}
