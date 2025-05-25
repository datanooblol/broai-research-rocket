// components/ui/AutoResizeTextarea.tsx
'use client'

import * as React from 'react'
import TextareaAutosize from 'react-textarea-autosize'
import type { TextareaAutosizeProps } from 'react-textarea-autosize'
import { cn } from '@/lib/utils'

// Extend and override style typing
type FixedTextareaProps = TextareaAutosizeProps & {
  style?: React.CSSProperties
}

export const AutoResizeTextarea = React.forwardRef<
  HTMLTextAreaElement,
  FixedTextareaProps
>(({ className, minRows = 1, maxRows = 10, ...props }, ref) => {
  return (
    <TextareaAutosize
      ref={ref}
      minRows={minRows}
      maxRows={maxRows}
      className={cn(
        'w-full min-w-full rounded-md border border-input bg-background px-3 py-2 text-sm shadow-sm placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 resize-none',
        className
      )}
      {...props}
    />
  )
})

AutoResizeTextarea.displayName = 'AutoResizeTextarea'
