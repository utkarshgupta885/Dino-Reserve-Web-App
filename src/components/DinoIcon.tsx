import React from 'react';

interface DinoIconProps {
  type: 'trex' | 'stego' | 'brachio' | 'raptor' | 'tricera';
  size?: 'sm' | 'md' | 'lg';
  className?: string;
}

export function DinoIcon({ type, size = 'md', className = '' }: DinoIconProps) {
  const sizeClasses = {
    sm: 'w-6 h-6',
    md: 'w-8 h-8',
    lg: 'w-12 h-12'
  };

  const dinoEmojis = {
    trex: '🦖',
    stego: '🦕',
    brachio: '🦕',
    raptor: '🦖',
    tricera: '🦕'
  };

  return (
    <div className={`${sizeClasses[size]} ${className} flex items-center justify-center text-2xl`}>
      {dinoEmojis[type]}
    </div>
  );
}