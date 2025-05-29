'use client';

import { useRouter } from 'next/navigation';
import { LogOut } from 'lucide-react';
import { Button } from '@/components/ui/button';

export default function LogoutButton() {
  const router = useRouter();

  const handleLogout = () => {
    router.push('/login');    // Redirect to login
  };

  return (
    <a href="/login" className="flex items-center gap-2">
      <LogOut className="w-4 h-4" />
      <span>Logout</span> 
    </a>
  );
}
