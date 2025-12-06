import React, { useState } from 'react';
import { chatAPI } from '../api/client';
import { FaSearch, FaCar } from 'react-icons/fa';

const FineVerifier = () => {
  const [vehicleNumber, setVehicleNumber] = useState('');
  const [violationType, setViolationType] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleVerify = async (e) => {
    e.preventDefault();
    
    if (!vehicleNumber || !violationType) {
      setError('Please provide both vehicle number and violation type');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await chatAPI.verifyFine(vehicleNumber, violationType);
      setResult(response);
    } catch (err) {
      setError(err.response?.data?.detail || 'Error verifying fine. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fine-verifier">
      <h2>
        <FaSearch /> Fine Verification
      </h2>
      <p className="description">
        Check fine amounts for traffic violations in Maharashtra
      </p>

      <form onSubmit={handleVerify}>
        <div className="form-group">
          <label htmlFor="vehicleNumber">
            <FaCar /> Vehicle Number
          </label>
          <input
            id="vehicleNumber"
            type="text"
            placeholder="e.g., MH01AB1234"
            value={vehicleNumber}
            onChange={(e) => setVehicleNumber(e.target.value.toUpperCase())}
            disabled={loading}
          />
        </div>

        <div className="form-group">
          <label htmlFor="violationType">Violation Type</label>
          <input
            id="violationType"
            type="text"
            placeholder="e.g., speeding, no helmet, signal jump"
            value={violationType}
            onChange={(e) => setViolationType(e.target.value)}
            disabled={loading}
          />
        </div>

        <button type="submit" disabled={loading}>
          {loading ? 'Verifying...' : 'Verify Fine'}
        </button>
      </form>

      {error && (
        <div className="error-message">
          <p>{error}</p>
        </div>
      )}

      {result && (
        <div className="fine-result">
          <h3>Fine Details</h3>
          <div className="result-item">
            <strong>Vehicle:</strong> {result.vehicle_number}
          </div>
          <div className="result-item">
            <strong>Violation:</strong> {result.violation_type}
          </div>
          <div className="result-item">
            <strong>Fine Amount:</strong> ₹{result.fine_amount}
          </div>
          <div className="result-item">
            <strong>Section:</strong> {result.applicable_section}
          </div>
          <div className="result-item">
            <strong>Description:</strong> {result.description}
          </div>
          {result.payment_link && (
            <div className="result-item">
              <a href={result.payment_link} target="_blank" rel="noopener noreferrer">
                Pay Online →
              </a>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default FineVerifier;
