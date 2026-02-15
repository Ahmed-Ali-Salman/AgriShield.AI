'use client';
import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Input } from '@/components/ui/Input';
import { Button } from '@/components/ui/Button';
import { authService } from '@/services/authService';

export default function RegisterPage() {
  const [form, setForm] = useState({ email: '', password: '', full_name: '' });
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await authService.register(form);
      localStorage.setItem('access_token', res.data.access_token);
      router.push('/dashboard');
    } catch { /* handle error */ }
    finally { setLoading(false); }
  };

  return (
    <div className='auth-page'>
      <form className='auth-form' onSubmit={handleSubmit}>
        <h1>Create Account</h1>
        <Input label='Full Name' value={form.full_name} onChange={e => setForm({...form, full_name: e.target.value})} required />
        <Input label='Email' type='email' value={form.email} onChange={e => setForm({...form, email: e.target.value})} required />
        <Input label='Password' type='password' value={form.password} onChange={e => setForm({...form, password: e.target.value})} required />
        <Button type='submit' loading={loading}>Register</Button>
      </form>
    </div>
  );
}
