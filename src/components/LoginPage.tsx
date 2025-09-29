import React, { useState } from 'react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { ImageWithFallback } from './figma/ImageWithFallback';

interface LoginPageProps {
  onLogin: () => void;
}

export function LoginPage({ onLogin }: LoginPageProps) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Simple validation for demo
    if (email && password) {
      onLogin();
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 via-orange-50 to-yellow-50 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <div className="inline-flex items-center gap-2 mb-4">
            <span className="text-4xl">🦕</span>
            <h1 className="text-4xl font-bold text-green-700">Dino Reserve</h1>
            <span className="text-4xl">🦖</span>
          </div>
          <p className="text-gray-600">Welcome to your prehistoric dining manager!</p>
        </div>

        <Card className="shadow-lg border-2 border-green-200">
          <CardHeader className="text-center">
            <div className="mx-auto mb-4 w-24 h-24 bg-green-100 rounded-full flex items-center justify-center">
              <ImageWithFallback 
                src="https://images.unsplash.com/photo-1728848447975-dc7f2aad30af?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxjdXRlJTIwY2FydG9vbiUyMGRpbm9zYXVyJTIwaWxsdXN0cmF0aW9ufGVufDF8fHx8MTc1OTE0MDczMnww&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral"
                alt="Cute dino mascot"
                className="w-16 h-16 object-cover rounded-full"
              />
            </div>
            <CardTitle className="text-green-700">Manager Login</CardTitle>
            <CardDescription>
              Sign in to manage your dino dining reservations
            </CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="email">Email</Label>
                <Input
                  id="email"
                  type="email"
                  placeholder="manager@dinoreserve.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="border-green-200 focus:border-green-400"
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="password">Password</Label>
                <Input
                  id="password"
                  type="password"
                  placeholder="••••••••"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="border-green-200 focus:border-green-400"
                />
              </div>
              <Button 
                type="submit" 
                className="w-full bg-green-600 hover:bg-green-700 text-white"
              >
                🦕 Enter Dino Reserve 🦖
              </Button>
            </form>
          </CardContent>
        </Card>

        <div className="text-center mt-6">
          <p className="text-sm text-gray-500 flex items-center justify-center gap-1">
            <span>🥬</span>
            Powered by prehistoric technology
            <span>🥬</span>
          </p>
        </div>
      </div>
    </div>
  );
}