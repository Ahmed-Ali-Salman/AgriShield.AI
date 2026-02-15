import React from 'react';

interface Column<T> { key: keyof T; header: string; render?: (value: any, row: T) => React.ReactNode; }

interface TableProps<T> { columns: Column<T>[]; data: T[]; onRowClick?: (row: T) => void; }

export function Table<T extends Record<string, any>>({ columns, data, onRowClick }: TableProps<T>) {
  return (
    <table className='table'>
      <thead>
        <tr>{columns.map(col => <th key={String(col.key)}>{col.header}</th>)}</tr>
      </thead>
      <tbody>
        {data.map((row, i) => (
          <tr key={i} onClick={() => onRowClick?.(row)} className={onRowClick ? 'clickable' : ''}>
            {columns.map(col => <td key={String(col.key)}>{col.render ? col.render(row[col.key], row) : String(row[col.key] ?? '')}</td>)}
          </tr>
        ))}
      </tbody>
    </table>
  );
}
