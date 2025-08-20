'use client';
import React from 'react';
import { motion } from 'framer-motion';
import { cn } from '@/lib/utils';

export const BackgroundBeams = ({
  className,
}: {
  className?: string;
}) => {
  const randomMove = () => Math.random() * 4 - 2;
  const randomOpacity = () => Math.random() * 0.5 + 0.5;
  const randomPath = () =>
    `M${Math.random() * 100},${Math.random() * 100} C${
      Math.random() * 100 + randomMove()
    },${Math.random() * 100 + randomMove()} ${
      Math.random() * 100 + randomMove()
    },${Math.random() * 100 + randomMove()} ${
      Math.random() * 100
    },${Math.random() * 100}`;

  return (
    <div
      className={cn(
        'absolute top-0 left-0 w-full h-full z-0 overflow-hidden',
        className
      )}
    >
      <svg
        className="w-full h-full"
        xmlns="http://www.w3.org/2000/svg"
        preserveAspectRatio="xMidYMid slice"
      >
        <defs>
          <radialGradient
            id="gradient"
            cx="50%"
            cy="50%"
            r="50%"
            fx="50%"
            fy="50%"
          >
            <stop offset="0%" stopColor="rgba(var(--color-one), 0.2)" />
            <stop offset="100%" stopColor="rgba(var(--color-one), 0)" />
          </radialGradient>
        </defs>
        {[...Array(10)].map((_, i) => (
          <motion.path
            key={`path-${i}`}
            d={randomPath()}
            stroke="url(#gradient)"
            strokeWidth="2"
            fill="none"
            initial={{ opacity: 0, pathLength: 0 }}
            animate={{
              opacity: [0, randomOpacity(), 0],
              pathLength: [0, 1, 0],
            }}
            transition={{
              duration: Math.random() * 10 + 5,
              repeat: Infinity,
              repeatType: 'loop',
              ease: 'linear',
              delay: Math.random() * -28,
            }}
          />
        ))}
      </svg>
    </div>
  );
};
