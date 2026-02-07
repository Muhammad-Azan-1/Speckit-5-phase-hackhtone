/**
 * Email Service
 * 
 * Handles sending emails for authentication flows.
 * Uses Resend for email delivery.
 */
import { Resend } from 'resend';

// Initialize Resend with API key
const resend = new Resend(process.env.RESEND_API_KEY);

interface EmailOptions {
  to: string;
  subject: string;
  text: string;
  html?: string;
}

export async function sendEmail(options: EmailOptions): Promise<void> {
  try {
    // Determine sender address
    // If you haven't verified a domain in Resend, you MUST use 'onboarding@resend.dev'
    // Once verified, change this to 'noreply@yourdomain.com'
    const from = 'Todo App <onboarding@resend.dev>';

    // Verify API Key availability (don't log the actual key)
    const key = process.env.RESEND_API_KEY;
    // console.log("Resend API Key loaded:", key ? "YES" : "NO");
    // console.log("Key starts with:", key ? `'${key.substring(0, 4)}...'` : "N/A"); // Check for quotes
    // console.log("Sending email to:", options.to);

    const { data, error } = await resend.emails.send({
      from,
      to: options.to,
      subject: options.subject,
      text: options.text,
      html: options.html,
    });

    if (error) {
      console.error("Resend API Returned Error:", error); // Log the full error object
      throw new Error(`Failed to send email: ${error.message}`);
    }

    console.log(`📧 Email sent successfully to ${options.to} (ID: ${data?.id})`);
  } catch (err) {
    console.error("Failed to send email catch block:", err);
    // Fallback to file logging in case of API failure (optional, but good for debugging)
    logEmailToFile(options);
  }
}

// Fallback logger
function logEmailToFile(options: EmailOptions) {
  try {
    const fs = require('fs');
    const path = require('path');
    const logPath = path.join(process.cwd(), 'email-debug.log');
    const timestamp = new Date().toISOString();
    const logEntry = `\n\n[${timestamp}] [FALLBACK LOG] TO: ${options.to}\nSUBJECT: ${options.subject}\nBODY:\n${options.text}\n----------------------------------------`;
    fs.appendFileSync(logPath, logEntry);
  } catch (err) {
    console.error("Failed to write email to log file:", err);
  }
}

export async function sendVerificationEmail(
  email: string,
  verificationUrl: string
): Promise<void> {
  await sendEmail({
    to: email,
    subject: "Verify your email address - Todo App",
    text: `
Hello!

Please verify your email address by clicking the link below:

${verificationUrl}

This link will expire in 24 hours.

If you didn't create an account, you can safely ignore this email.

Thanks,
Todo App Team
    `.trim(),
    html: `
<!DOCTYPE html>
<html>
<head>
  <style>
    body { font-family: system-ui, -apple-system, sans-serif; }
    .container { max-width: 600px; margin: 0 auto; padding: 20px; }
    .button { 
      display: inline-block; 
      background: #000; 
      color: #fff !important; 
      padding: 12px 24px; 
      text-decoration: none; 
      border-radius: 8px; 
      margin: 20px 0;
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>Verify your email</h1>
    <p>Please verify your email address by clicking the button below:</p>
    <a href="${verificationUrl}" class="button">Verify Email</a>
    <p>Or copy and paste this link:</p>
    <p>${verificationUrl}</p>
    <p>This link will expire in 24 hours.</p>
    <p>If you didn't create an account, you can safely ignore this email.</p>
  </div>
</body>
</html>
    `.trim(),
  });
}
