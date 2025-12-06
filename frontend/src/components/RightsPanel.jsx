import React from 'react';
import { FaBalanceScale, FaPhoneAlt, FaExclamationTriangle } from 'react-icons/fa';

const RightsPanel = () => {
  return (
    <div className="rights-panel">
      <h2>
        <FaBalanceScale /> Your Rights
      </h2>
      
      <div className="rights-section">
        <h3>During Traffic Stop</h3>
        <ul>
          <li>Right to know the reason for being stopped</li>
          <li>Right to see the officer's ID card</li>
          <li>Right to polite and professional treatment</li>
          <li>Right to receive a copy of the challan</li>
          <li>Right to contest the challan in court</li>
        </ul>
      </div>

      <div className="rights-section">
        <h3>Important Contacts</h3>
        <div className="contact-item">
          <FaPhoneAlt />
          <div>
            <strong>Mumbai Traffic Police:</strong> 103
          </div>
        </div>
        <div className="contact-item">
          <FaPhoneAlt />
          <div>
            <strong>Anti-Corruption Bureau:</strong> 1064
          </div>
        </div>
        <div className="contact-item">
          <FaPhoneAlt />
          <div>
            <strong>Emergency:</strong> 112
          </div>
        </div>
      </div>

      <div className="rights-section">
        <h3>Online Resources</h3>
        <ul>
          <li>
            <a href="https://mahatrafficechallan.gov.in" target="_blank" rel="noopener noreferrer">
              Maharashtra Traffic E-Challan Portal
            </a>
          </li>
          <li>
            <a href="https://parivahan.gov.in" target="_blank" rel="noopener noreferrer">
              National Parivahan Portal
            </a>
          </li>
        </ul>
      </div>

      <div className="warning-box">
        <FaExclamationTriangle />
        <p>
          <strong>Note:</strong> This chatbot provides general information only. 
          For specific legal matters, consult a qualified legal professional.
        </p>
      </div>
    </div>
  );
};

export default RightsPanel;
