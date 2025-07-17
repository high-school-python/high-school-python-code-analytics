'use client'

import { useEffect, useState } from 'react'
import toast from 'react-hot-toast'
import { api } from '@/lib/api-client'
import type { AnalyzeResponse, Improvement, StyleIssue } from '@/lib/api-types'

interface AnalysisPanelProps {
  code: string
  shouldAnalyze?: boolean
  onAnalyzeComplete?: () => void
}

export default function AnalysisPanel({ code, shouldAnalyze, onAnalyzeComplete }: AnalysisPanelProps) {
  const [analysis, setAnalysis] = useState<AnalyzeResponse | null>(null)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    const analyzeCode = async () => {
      if (!code.trim() || code === '# Pythonコードをここに入力してください\n') {
        setAnalysis(null)
        return
      }

      setLoading(true)

      try {
        const result = await api.analyzeCode({ code })
        console.log(result)
        setAnalysis(result)
      } catch (error) {
        console.error('Analysis error:', error)
        toast.error('コードの解析中にエラーが発生しました')
      } finally {
        setLoading(false)
        if (onAnalyzeComplete) {
          onAnalyzeComplete()
        }
      }
    }

    if (shouldAnalyze) analyzeCode()
  }, [code, shouldAnalyze, onAnalyzeComplete])

  if (loading) {
    return (
      <div className='text-center py-8'>
        <div className='inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500' />
        <p className='mt-2 text-gray-500'>解析中...</p>
      </div>
    )
  }

  if (!analysis) {
    return (
      <div className='text-center py-12'>
        <div className='text-6xl mb-4'>🧑‍💻</div>
        <p className='text-gray-400'>コードを入力して解析ボタンを押してください</p>
      </div>
    )
  }

  if (!analysis.success) {
    return (
      <div className='bg-red-50 border-2 border-red-200 rounded-xl p-4'>
        <h3 className='font-bold text-red-800 mb-2 flex items-center gap-2'>
          <span className='text-xl'>⚠️</span>
          構文エラー
        </h3>
        <p className='text-red-700'>{analysis.message}</p>
        {analysis.line && (
          <p className='text-sm text-red-600 mt-2 font-mono bg-red-100 px-2 py-1 rounded'>
            行 {analysis.line}: {analysis.text}
          </p>
        )}
        <div className='mt-4 p-3 bg-red-100 rounded-lg'>
          <p className='text-sm text-red-800 font-medium flex items-start gap-2'>
            <span className='text-lg'>💡</span>
            <span>
              このエラーメッセージをコピーして、「エラーを解析する」タブで詳しく見てみましょう！
              <br />
              エラーの原因と解決方法を分かりやすく説明します。
            </span>
          </p>
        </div>
      </div>
    )
  }

  return (
    <div className='space-y-4'>
      {/* 品質スコア */}
      <div className='bg-gradient-to-br from-blue-50 to-blue-100 border-2 border-blue-200 rounded-xl p-6 relative overflow-hidden'>
        <div className='absolute top-0 right-0 text-8xl opacity-10'>🏆</div>
        <h3 className='font-bold text-blue-800 mb-3 flex items-center gap-2'>
          <span className='text-xl'>⭐</span>
          コード品質スコア
        </h3>
        <div className='text-4xl font-bold text-blue-600'>{analysis.summary?.quality_score || 0}/100</div>
        <p className='text-sm text-blue-700 mt-2'>
          問題: {analysis.summary?.total_issues || 0}件 • 改善提案: {analysis.summary?.total_suggestions || 0}件
        </p>
      </div>

      {/* 統計情報 */}
      <div className='bg-gradient-to-br from-gray-50 to-gray-100 rounded-xl p-5 border border-gray-200'>
        <h3 className='font-bold mb-3 flex items-center gap-2'>
          <span className='text-xl'>📊</span>
          統計情報
        </h3>
        <div className='grid grid-cols-2 gap-3'>
          <div className='bg-white rounded-lg p-3 text-center'>
            <div className='text-2xl font-bold text-gray-800'>{analysis.stats?.total_lines || 0}</div>
            <div className='text-xs text-gray-600'>総行数</div>
          </div>
          <div className='bg-white rounded-lg p-3 text-center'>
            <div className='text-2xl font-bold text-gray-800'>{analysis.stats?.code_lines || 0}</div>
            <div className='text-xs text-gray-600'>コード行数</div>
          </div>
          <div className='bg-white rounded-lg p-3 text-center'>
            <div className='text-2xl font-bold text-gray-800'>{analysis.stats?.function_count || 0}</div>
            <div className='text-xs text-gray-600'>関数数</div>
          </div>
          <div className='bg-white rounded-lg p-3 text-center'>
            <div className='text-2xl font-bold text-gray-800'>{analysis.stats?.class_count || 0}</div>
            <div className='text-xs text-gray-600'>クラス数</div>
          </div>
        </div>
      </div>

      {/* スタイルの問題 */}
      {analysis.style_issues && analysis.style_issues.length > 0 && (
        <div className='bg-gradient-to-br from-yellow-50 to-orange-50 border-2 border-yellow-200 rounded-xl p-5'>
          <h3 className='font-bold text-yellow-800 mb-3 flex items-center gap-2'>
            <span className='text-xl'>💡</span>
            スタイルの問題
          </h3>
          <ul className='space-y-2'>
            {analysis.style_issues.map((issue: StyleIssue, index: number) => (
              <li key={index} className='bg-white rounded-lg p-3 flex items-start gap-2'>
                <span className='text-yellow-600 font-mono text-xs bg-yellow-100 px-2 py-1 rounded'>
                  行 {issue.line}
                </span>
                <span className='text-gray-700 text-sm flex-1'>{issue.message}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* 改善提案 */}
      {analysis.improvements && analysis.improvements.length > 0 && (
        <div className='bg-gradient-to-br from-green-50 to-emerald-50 border-2 border-green-200 rounded-xl p-5'>
          <h3 className='font-bold text-green-800 mb-3 flex items-center gap-2'>
            <span className='text-xl'>🌱</span>
            改善提案
          </h3>
          <ul className='space-y-2'>
            {analysis.improvements.map((improvement: Improvement, index: number) => (
              <li key={index} className='bg-white rounded-lg p-3 flex items-start gap-2'>
                <span className='text-green-600 text-lg'>✓</span>
                <span className='text-gray-700 text-sm'>{improvement.message}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}
