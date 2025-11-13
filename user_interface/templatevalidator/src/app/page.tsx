// app/page.tsx
'use client';

import { useState, FormEvent } from 'react';
import styles from './page.module.css';

// Define the shape of the API response
type TicketResponse = {
  ticket_number: string;
  result: any[];
  status: string;
};

export default function AutomationValidator() {
  // === Form State ===
  // Pre-filled with example data from your Pydantic model
  const [ticketNumber, setTicketNumber] = useState('INC123456');
  const [automationName, setAutomationName] = useState('Purchase Order Processing for Vendor X');
  const [requestedBy, setRequestedBy] = useState('john.doe@example.com');
  const [templateUrls, setTemplateUrls] = useState('http://example.com/template1\nhttp://example.com/template2');
  const [status, setStatus] = useState('Open');

  // === API State ===
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [successResponse, setSuccessResponse] = useState<TicketResponse | null>(null);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);
    setSuccessResponse(null);

    // 1. Transform the textarea string into an array of strings
    const urls = templateUrls.split('\n').filter(url => url.trim() !== '');

    if (urls.length === 0) {
      setError('Please provide at least one template URL.');
      setIsLoading(false);
      return;
    }

    // 2. Build the request body matching the FastAPI model
    const requestBody = {
      ticket_number: ticketNumber,
      automation_name: automationName,
      status: status,
      requested_by: requestedBy,
      template_urls: urls,
    };

    // 3. Make the API call
    try {
      const response = await fetch('http://127.0.0.1:8000/api/v1/process-ticket', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
      });

      if (!response.ok) {
        // Try to parse the error detail from FastAPI
        const errData = await response.json();
        throw new Error(errData.detail || 'An unknown error occurred.');
      }

      const data: TicketResponse = await response.json();
      setSuccessResponse(data);

    } catch (err: any) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main className={styles.container}>
      <div className={styles.card}>
        <h1 className={styles.title}>Automation Template Validation</h1>
        <p className={styles.subtitle}>
          Submit an existing ticket to validate its automation templates.
        </p>

        <form onSubmit={handleSubmit} className={styles.form}>
          <div className={styles.formGroup}>
            <label htmlFor="ticketNumber" className={styles.label}>
              Ticket Number
            </label>
            <input
              id="ticketNumber"
              type="text"
              value={ticketNumber}
              onChange={(e) => setTicketNumber(e.target.value)}
              className={styles.input}
              required
            />
          </div>

          <div className={styles.formGroup}>
            <label htmlFor="automationName" className={styles.label}>
              Automation Name
            </label>
            <input
              id="automationName"
              type="text"
              value={automationName}
              onChange={(e) => setAutomationName(e.target.value)}
              className={styles.input}
              required
            />
          </div>

          <div className={styles.formRow}>
            <div className={styles.formGroup}>
              <label htmlFor="requestedBy" className={styles.label}>
                Requested By (Email)
              </label>
              <input
                id="requestedBy"
                type="email"
                value={requestedBy}
                onChange={(e) => setRequestedBy(e.target.value)}
                className={styles.input}
                required
              />
            </div>
            <div className={styles.formGroup}>
              <label htmlFor="status" className={styles.label}>
                Status
              </label>
              <input
                id="status"
                type="text"
                value={status}
                onChange={(e) => setStatus(e.target.value)}
                className={styles.input}
                required
              />
            </div>
          </div>

          <div className={styles.formGroup}>
            <label htmlFor="templateUrls" className={styles.label}>
              Template URLs (one per line)
            </label>
            <textarea
              id="templateUrls"
              value={templateUrls}
              onChange={(e) => setTemplateUrls(e.target.value)}
              className={styles.textarea}
              rows={4}
              required
            />
          </div>

          <button type="submit" className={styles.button} disabled={isLoading}>
            {isLoading ? 'Processing...' : 'Submit for Validation'}
          </button>
        </form>

        {/* === API Response Section === */}
        {error && (
          <div className={styles.errorBox}>
            <strong>Error:</strong> {error}
          </div>
        )}

        {successResponse && (
          <div className={styles.successBox}>
            <strong>Validation Processed (Ticket: {successResponse.ticket_number})</strong>
            <p>Status: {successResponse.status}</p>
            <div className={styles.resultBox}>
              <p>Agent Result:</p>
              <pre>
                {JSON.stringify(successResponse.result, null, 2)}
              </pre>
            </div>
          </div>
        )}
      </div>
    </main>
  );
}