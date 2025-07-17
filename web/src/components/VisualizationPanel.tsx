'use client'

import { useEffect, useState } from 'react'
import toast from 'react-hot-toast'
import { api } from '@/lib/api-client'
import type { SimulatedStep, StepExplanation, VisualizeResponse } from '@/lib/api-types'

interface VisualizationPanelProps {
  code: string
  shouldAnalyze?: boolean
  onAnalyzeComplete?: () => void
}

export default function VisualizationPanel({ code, shouldAnalyze, onAnalyzeComplete }: VisualizationPanelProps) {
  const [visualization, setVisualization] = useState<VisualizeResponse | null>(null)
  const [loading, setLoading] = useState(false)
  const [highlightLine, setHighlightLine] = useState<number | null>(null)

  useEffect(() => {
    const visualizeCode = async () => {
      if (!code.trim() || code === '# Pythonコードをここに入力してください\n') {
        setVisualization(null)
        return
      }

      setLoading(true)
      try {
        const result = await api.visualizeCode({
          code,
          highlight_line: highlightLine !== null ? highlightLine : undefined,
          show_flow: true,
        })
        console.log(result)
        setVisualization(result)
      } catch (error) {
        console.error('Visualization error:', error)
        toast.error('可視化中にエラーが発生しました')
      } finally {
        setLoading(false)
        if (onAnalyzeComplete) onAnalyzeComplete()
      }
    }

    if (shouldAnalyze) visualizeCode()
  }, [code, shouldAnalyze, highlightLine, onAnalyzeComplete])

  if (loading) {
    return (
      <div className='text-center py-8'>
        <div className='inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500' />
        <p className='mt-2 text-gray-500'>可視化中...</p>
      </div>
    )
  }

  if (!visualization) {
    return (
      <div className='text-center py-12'>
        <div className='text-6xl mb-4'>🎨</div>
        <p className='text-gray-400'>コードを入力して解析ボタンを押してください</p>
      </div>
    )
  }

  if (!visualization.success) {
    return (
      <div className='bg-red-50 border-2 border-red-200 rounded-xl p-4'>
        <h3 className='font-bold text-red-800 mb-2 flex items-center gap-2'>
          <span className='text-xl'>⚠️</span>
          エラー
        </h3>
        <p className='text-red-700'>{visualization.message}</p>
        <div className='mt-4 p-3 bg-red-100 rounded-lg'>
          <p className='text-sm text-red-800 font-medium flex items-start gap-2'>
            <span className='text-lg'>💡</span>
            <span>
              エラーが発生しました！まずは「コードを解析する」タブでエラーを分析し、問題を解決してから戻ってきましょう。
              <br />
              エラーメッセージをコピーして、「エラーを解析する」タブに貼り付けてください。
            </span>
          </p>
        </div>
      </div>
    )
  }

  return (
    <div className='space-y-4'>
      {/* フローチャート */}
      {visualization.flowchart && (
        <div className='bg-gradient-to-br from-blue-50 to-purple-50 border-2 border-blue-200 rounded-xl p-5'>
          <h3 className='font-bold mb-3 flex items-center gap-2'>
            <span className='text-xl'>🌐</span>
            実行フロー図
          </h3>
          <div
            className='bg-white rounded-lg p-4 overflow-auto'
            dangerouslySetInnerHTML={{ __html: visualization.flowchart }}
          />
        </div>
      )}

      {/* 実行ステップ */}
      <div className='bg-gradient-to-br from-gray-50 to-gray-100 rounded-xl p-5 border border-gray-200'>
        <h3 className='font-bold mb-3 flex items-center gap-2'>
          <span className='text-xl'>👣</span>
          実行ステップ
        </h3>
        <div className='space-y-2 max-h-96 overflow-y-auto'>
          {visualization.steps.map((step: SimulatedStep, index: number) => (
            <div
              key={index}
              role='button'
              tabIndex={0}
              className={`p-3 rounded-lg text-sm transition-all duration-200 ${
                highlightLine !== null && (step.line || step.line_number) === highlightLine
                  ? 'bg-yellow-100 border-yellow-300 shadow-md'
                  : 'bg-white border-gray-200'
              } border hover:shadow-md cursor-pointer`}
              onClick={() => setHighlightLine(step.line || step.line_number)}
              onKeyDown={(e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                  e.preventDefault()
                  setHighlightLine(step.line || step.line_number)
                }
              }}
            >
              <div className='flex justify-between items-start'>
                <div className='flex-1'>
                  <span className='text-gray-500 font-mono text-xs bg-gray-100 px-2 py-1 rounded'>
                    行 {step.line || step.line_number}
                  </span>{' '}
                  <code className='text-blue-600 font-semibold'>{step.description}</code>
                </div>
                <span className='text-xs text-gray-400 ml-2 bg-gray-100 px-2 py-1 rounded'>{step.action}</span>
              </div>
              {step.variables && Object.keys(step.variables).length > 0 && (
                <div className='mt-1 text-xs text-gray-600'>変数: {JSON.stringify(step.variables)}</div>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* 説明 */}
      {visualization.explanations && (
        <div className='bg-gradient-to-br from-blue-50 to-cyan-50 border-2 border-blue-200 rounded-xl p-5'>
          <h3 className='font-bold text-blue-800 mb-3 flex items-center gap-2'>
            <span className='text-xl'>💡</span>
            ステップの説明
          </h3>
          <div className='space-y-3'>
            {visualization.explanations.slice(0, 5).map((exp: StepExplanation, index: number) => (
              <div key={index} className='bg-white rounded-lg p-3 flex items-start gap-2'>
                <span className='text-blue-600 font-mono text-xs bg-blue-100 px-2 py-1 rounded'>行 {exp.line}</span>
                <span className='text-gray-700 text-sm flex-1'>{exp.explanation}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
