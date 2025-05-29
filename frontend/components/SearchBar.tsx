'use client';

import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import React from 'react';

type SearchBarProps = {
  value: string;
  onChange: (value: string) => void;
  placeholder?: string;
  label?: string;
};

export default function SearchBar({
  value,
  onChange,
  placeholder = 'Type keyword...',
  label = 'Filter by context',
}: SearchBarProps) {
  return (
    <div className="mb-6">
      <Label htmlFor="filter">{label}</Label>
      <Input
        id="filter"
        placeholder={placeholder}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="mt-2"
      />
    </div>
  );
}
