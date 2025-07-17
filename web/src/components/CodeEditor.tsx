'use client'

import dynamic from 'next/dynamic'
import { useEffect, useState } from 'react'

const Editor = dynamic(() => import('@monaco-editor/react'), { ssr: false })

interface CodeEditorProps {
  value: string
  onChange: (value: string) => void
}

export default function CodeEditor({ value, onChange }: CodeEditorProps) {
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    setMounted(true)
  }, [])

  if (!mounted) {
    return (
      <div className='h-[400px] flex items-center justify-center bg-gray-50 rounded border'>
        <p className='text-gray-500'>エディタを読み込み中...</p>
      </div>
    )
  }

  return (
    <Editor
      height='400px'
      defaultLanguage='python'
      value={value}
      onChange={(value) => onChange(value || '')}
      theme='vs-light'
      options={{
        minimap: { enabled: false },
        fontSize: 14,
        wordWrap: 'on',
        automaticLayout: true,
        scrollBeyondLastLine: false,
      }}
    />
  )
}
