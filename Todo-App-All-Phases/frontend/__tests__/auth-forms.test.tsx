// Test file for authentication forms
// This is a sample test to verify the authentication forms work correctly

import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { RegisterForm } from '@/components/forms/register-form';
import { LoginForm } from '@/components/forms/login-form';

describe('Authentication Forms', () => {
  describe('RegisterForm', () => {
    it('should render the registration form with all fields', () => {
      render(<RegisterForm />);

      expect(screen.getByLabelText(/name/i)).toBeInTheDocument();
      expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
      expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
      expect(screen.getByRole('button', { name: /sign up/i })).toBeInTheDocument();
    });

    it('should show validation errors for invalid input', async () => {
      render(<RegisterForm />);

      // Submit empty form
      fireEvent.click(screen.getByRole('button', { name: /sign up/i }));

      await waitFor(() => {
        expect(screen.getByText(/name must be at least 2 characters long/i)).toBeInTheDocument();
        expect(screen.getByText(/please enter a valid email address/i)).toBeInTheDocument();
        expect(screen.getByText(/password must be at least 8 characters long/i)).toBeInTheDocument();
      });
    });

    it('should accept valid registration data', async () => {
      render(<RegisterForm />);

      // Fill in valid data
      fireEvent.change(screen.getByLabelText(/name/i), { target: { value: 'John Doe' } });
      fireEvent.change(screen.getByLabelText(/email/i), { target: { value: 'john@example.com' } });
      fireEvent.change(screen.getByLabelText(/password/i), { target: { value: 'Password123' } });

      // Submit the form
      fireEvent.click(screen.getByRole('button', { name: /sign up/i }));

      await waitFor(() => {
        expect(screen.queryByText(/name must be at least 2 characters long/i)).not.toBeInTheDocument();
        expect(screen.queryByText(/please enter a valid email address/i)).not.toBeInTheDocument();
        expect(screen.queryByText(/password must be at least 8 characters long/i)).not.toBeInTheDocument();
      });
    });
  });

  describe('LoginForm', () => {
    it('should render the login form with all fields', () => {
      render(<LoginForm />);

      expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
      expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
      expect(screen.getByRole('button', { name: /sign in/i })).toBeInTheDocument();
    });

    it('should show validation errors for invalid login', async () => {
      render(<LoginForm />);

      // Submit empty form
      fireEvent.click(screen.getByRole('button', { name: /sign in/i }));

      await waitFor(() => {
        expect(screen.getByText(/please enter a valid email address/i)).toBeInTheDocument();
        expect(screen.getByText(/password is required/i)).toBeInTheDocument();
      });
    });

    it('should accept valid login credentials', async () => {
      render(<LoginForm />);

      // Fill in valid data
      fireEvent.change(screen.getByLabelText(/email/i), { target: { value: 'john@example.com' } });
      fireEvent.change(screen.getByLabelText(/password/i), { target: { value: 'Password123' } });

      // Submit the form
      fireEvent.click(screen.getByRole('button', { name: /sign in/i }));

      await waitFor(() => {
        expect(screen.queryByText(/please enter a valid email address/i)).not.toBeInTheDocument();
        expect(screen.queryByText(/password is required/i)).not.toBeInTheDocument();
      });
    });
  });
});