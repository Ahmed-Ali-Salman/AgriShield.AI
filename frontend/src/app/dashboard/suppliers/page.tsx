'use client';
import React, { useState, useRef } from 'react';
import { useRouter } from 'next/navigation';
import { useSuppliers } from '@/hooks/useSuppliers';
import { SupplierList } from '@/components/suppliers/SupplierList';
import { Loader } from '@/components/ui/Loader';
import { Button } from '@/components/ui/Button';
import { Card } from '@/components/ui/Card';
import { Modal } from '@/components/ui/Modal';
import { useToast } from '@/components/ui/Toast';
import api from '@/services/api';
import { Upload } from 'lucide-react';

export default function SuppliersPage() {
  const { suppliers, loading, refetch } = useSuppliers();
  const router = useRouter();
  const { toast } = useToast();
  const [showUpload, setShowUpload] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [dragOver, setDragOver] = useState(false);
  const fileRef = useRef<HTMLInputElement>(null);

  const handleUpload = async (file: File) => {
    setUploading(true);
    try {
      const formData = new FormData();
      formData.append('file', file);
      const res = await api.post('/data/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      const { created, total_rows, errors } = res.data;
      toast(`Imported ${created} of ${total_rows} suppliers`, errors.length ? 'warning' : 'success');
      if (errors.length) {
        console.warn('Upload errors:', errors);
      }
      setShowUpload(false);
      refetch();
    } catch (e: any) {
      toast(e.response?.data?.detail || 'Upload failed', 'error');
    } finally {
      setUploading(false);
    }
  };

  const onDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setDragOver(false);
    const file = e.dataTransfer.files[0];
    if (file) handleUpload(file);
  };

  if (loading) return <Loader />;

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
        <h1 className='page-title' style={{ margin: 0 }}>Suppliers</h1>
        <Button variant='primary' onClick={() => setShowUpload(true)}>
          <Upload size={16} style={{ marginRight: 8 }} /> Import CSV
        </Button>
      </div>

      <SupplierList
        suppliers={suppliers}
        onSelect={(s) => router.push(`/dashboard/suppliers/${s.id}`)}
      />

      {/* Upload Modal */}
      <Modal isOpen={showUpload} title='Import Suppliers' onClose={() => setShowUpload(false)}>
        <div
          className={`upload-zone ${dragOver ? 'drag-over' : ''}`}
          onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
          onDragLeave={() => setDragOver(false)}
          onDrop={onDrop}
          onClick={() => fileRef.current?.click()}
        >
          <Upload size={40} style={{ color: 'var(--color-text-muted)', marginBottom: 12 }} />
          <p style={{ color: 'var(--color-text-muted)', marginBottom: 8 }}>
            {uploading ? 'Uploading...' : 'Drop a CSV or Excel file here, or click to browse'}
          </p>
          <small style={{ color: 'var(--color-text-muted)' }}>
            Required columns: name, country · Optional: category, contact_email, website
          </small>
        </div>
        <input
          ref={fileRef}
          type='file'
          accept='.csv,.xls,.xlsx'
          style={{ display: 'none' }}
          onChange={(e) => {
            const file = e.target.files?.[0];
            if (file) handleUpload(file);
          }}
        />
      </Modal>
    </div>
  );
}
