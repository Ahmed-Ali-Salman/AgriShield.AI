'use client';
import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Input } from '@/components/ui/Input';
import { Button } from '@/components/ui/Button';
import { authService } from '@/services/authService';

export default function RegisterPage() {
  const [form, setForm] = useState({ email: '', password: '', full_name: '' });
  const [errors, setErrors] = useState<{ email?: string; password?: string; full_name?: string }>({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  const validate = () => {
    const newErrors: { email?: string; password?: string; full_name?: string } = {};
    if (!form.full_name.trim()) newErrors.full_name = 'Full name is required';
    if (!form.email) newErrors.email = 'Email is required';
    else if (!/\S+@\S+\.\S+/.test(form.email)) newErrors.email = 'Email is invalid';
    if (!form.password) newErrors.password = 'Password is required';
    else if (form.password.length < 8) newErrors.password = 'Password must be at least 8 characters';
    return newErrors;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const newErrors = validate();
    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    setLoading(true);
    setError(null);
    setErrors({});

    try {
      const res = await authService.register(form);
      localStorage.setItem('access_token', res.data.access_token);
      document.cookie = `auth_token=${res.data.access_token}; path=/; max-age=${60 * 60 * 24 * 7}; SameSite=Lax`;
      router.push('/dashboard');
    } catch (e: any) {
      setError(e.response?.data?.detail || 'Registration failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className='auth-page'>
      <form className='auth-form' onSubmit={handleSubmit}>
        <h1>Create Account</h1>
        <Input
          label='Full Name'
          value={form.full_name}
          onChange={e => { setForm({ ...form, full_name: e.target.value }); if (errors.full_name) setErrors({ ...errors, full_name: undefined }); }}
          error={errors.full_name}
          required
        />
        <Input
          label='Email'
          type='email'
          value={form.email}
          onChange={e => { setForm({ ...form, email: e.target.value }); if (errors.email) setErrors({ ...errors, email: undefined }); }}
          error={errors.email}
          required
        />
        <Input
          label='Password'
          type='password'
          value={form.password}
          onChange={e => { setForm({ ...form, password: e.target.value }); if (errors.password) setErrors({ ...errors, password: undefined }); }}
          error={errors.password}
          required
        />
        {error && <p style={{ color: 'var(--color-danger)', fontSize: '0.9rem', marginTop: '8px' }}>{error}</p>}
        <Button type='submit' loading={loading} style={{ marginTop: '16px' }}>Register</Button>
        <p style={{ textAlign: 'center', marginTop: '16px', color: 'var(--color-text-muted)', fontSize: '0.9rem' }}>
          Already have an account?{' '}
          <a href='/login' style={{ color: 'var(--color-primary)' }}>Sign in</a>
        </p>
      </form>
    </div>
  );
}
