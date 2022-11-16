//
//  UIViewExtension.swift
//  Electrodes
//
//  Created by Nick Varenbut on 11/15/22.
//

import Foundation
import UIKit

extension UIView {
    func getRoundedCorner(by value: CGFloat) {
        self.layer.cornerRadius = value
    }
    
    func getBorder(by value: CGFloat) {
        self.layer.borderWidth = value
        self.layer.borderColor = UIColor.black.cgColor
    }
}
