'use client';
import React from 'react';
import { Bell, User } from 'lucide-react';

export function Header() {
  return (
    <header className='header'>
      <div className='header-search'>
        <input type='search' placeholder='Search suppliers...' className='search-input' />
      </div>
      <div className='header-actions'>
        <button className='icon-btn'><Bell size={20} /></button>
        <button className='icon-btn'><User size={20} /></button>
      </div>
    </header>
  );
}
