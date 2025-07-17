'use client'

import { useEffect, useState } from 'react'
import toast from 'react-hot-toast'
import { api } from '@/lib/api-client'
import type { DebugStep, ErrorAnalyzeResponse, SimilarExample } from '@/lib/api-types'

interface ErrorAnalysisPanelProps {
  code: string
  shouldAnalyze?: boolean
  onAnalyzeComplete?: () => void
}

export default function ErrorAnalysisPanel({ code, shouldAnalyze, onAnalyzeComplete }: ErrorAnalysisPanelProps) {
  const [errorMessage, setErrorMessage] = useState('')
  const [analysis, setAnalysis] = useState<ErrorAnalyzeResponse | null>(null)
  const [loading, setLoading] = useState(false)

  const analyzeError = async () => {
    if (!code.trim() || !errorMessage.trim()) {
      if (onAnalyzeComplete) onAnalyzeComplete()

      return
    }

    setLoading(true)
    try {
      const result = await api.analyzeError({ code, error_message: errorMessage })
      console.log(result)
      setAnalysis(result)
    } catch (error) {
      console.error('Error analysis error:', error)
      toast.error('エラー解析中に問題が発生しました')
    } finally {
      setLoading(false)
      if (onAnalyzeComplete) onAnalyzeComplete()
    }
  }

  useEffect(() => {
    if (shouldAnalyze && errorMessage.trim()) {
      analyzeError()
    } else if (shouldAnalyze && onAnalyzeComplete) {
      onAnalyzeComplete()
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [shouldAnalyze])

  return (
    <div className='space-y-4'>
      <div>
        <label htmlFor='errorMessage' className='block text-sm font-bold text-gray-700 mb-2 flex items-center gap-2'>
          <span className='text-lg'>📨</span>
          エラーメッセージを入力
        </label>
        <textarea
          className='w-full p-3 border-2 border-gray-200 rounded-xl resize-none focus:border-blue-400 focus:outline-none transition-colors'
          rows={3}
          placeholder="例: NameError: name 'x' is not defined"
          value={errorMessage}
          onChange={(e) => setErrorMessage(e.target.value)}
        />
        <button
          type='button'
          onClick={analyzeError}
          disabled={loading}
          className='mt-3 w-full btn-primary text-white py-3 px-6 rounded-xl font-bold transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2'
        >
          {loading ? (
            <>
              <div className='animate-spin rounded-full h-5 w-5 border-b-2 border-white' />
              解析中...
            </>
          ) : (
            <>
              <span className='text-xl'>🔍</span>
              エラーを解析
            </>
          )}
        </button>
      </div>

      {analysis && (
        <div className='space-y-6'>
          {/* エラータイプと位置 */}
          <div className='bg-gradient-to-br from-red-50 to-red-100 border-2 border-red-200 rounded-xl p-5 shadow-lg'>
            <div className='flex items-start justify-between'>
              <div>
                <h3 className='font-bold text-red-800 text-xl mb-2 flex items-center gap-2'>
                  <span className='text-2xl'>⚠️</span>
                  {analysis.error_type}
                </h3>
                {analysis.line_number > 0 && (
                  <p className='text-sm text-red-600 font-mono bg-red-200/50 px-3 py-1 rounded inline-block'>
                    行 {analysis.line_number}
                    {analysis.column_number > 0 && `, 列 ${analysis.column_number}`}
                  </p>
                )}
              </div>
              {analysis.difficulty_level && (
                <div className='flex gap-1'>
                  {[...Array(3)].map((_, i) => (
                    <span
                      key={i}
                      className={`text-lg ${i < (analysis.difficulty_level ?? 0) ? 'text-red-500' : 'text-gray-300'}`}
                    >
                      ⭐
                    </span>
                  ))}
                </div>
              )}
            </div>
            <p className='text-gray-700 mt-3 font-medium'>{analysis.simple_explanation}</p>
          </div>

          {/* 詳細説明 */}
          <div className='bg-gradient-to-br from-blue-50 to-cyan-50 border-2 border-blue-200 rounded-xl p-5 shadow-lg'>
            <h3 className='font-bold text-blue-800 text-lg mb-3 flex items-center gap-2'>
              <span className='text-xl'>📚</span>
              詳しい説明
            </h3>
            <div className='space-y-3'>
              <p className='text-gray-700 bg-white/70 rounded-lg p-3'>{analysis.detailed_explanation}</p>
              {analysis.concept_explanation && (
                <div className='bg-blue-100/50 rounded-lg p-4 border border-blue-300'>
                  <p className='text-sm font-medium text-blue-900'>
                    <span className='text-lg mr-1'>💡</span>
                    {analysis.concept_explanation}
                  </p>
                </div>
              )}
              {analysis.common_causes && analysis.common_causes.length > 0 && (
                <div className='mt-3'>
                  <p className='font-bold text-sm mb-2 flex items-center gap-2'>
                    <span className='text-lg'>🔍</span>
                    確認ポイント:
                  </p>
                  <ul className='space-y-1'>
                    {analysis.common_causes.map((cause: string, index: number) => (
                      <li key={index} className='text-sm text-gray-700 flex items-start gap-2'>
                        <span className='text-blue-500 mt-0.5'>•</span>
                        <span>{cause}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </div>

          {/* 視覚的な説明 */}
          {analysis.visual_explanation && (
            <div className='bg-gradient-to-br from-purple-50 to-pink-50 border-2 border-purple-200 rounded-xl p-5 shadow-lg'>
              <h3 className='font-bold text-purple-800 text-lg mb-3 flex items-center gap-2'>
                <span className='text-xl'>🎨</span>
                視覚的な説明
              </h3>
              <pre className='bg-white/80 rounded-lg p-4 text-sm font-mono overflow-x-auto border border-purple-200'>
                {analysis.visual_explanation.content}
              </pre>
            </div>
          )}

          {/* ステップバイステップガイド */}
          {analysis.step_by_step_guide && analysis.step_by_step_guide.length > 0 && (
            <div className='bg-gradient-to-br from-yellow-50 to-orange-50 border-2 border-yellow-200 rounded-xl p-5 shadow-lg'>
              <h3 className='font-bold text-yellow-800 text-lg mb-3 flex items-center gap-2'>
                <span className='text-xl'>📋</span>
                解決手順
              </h3>
              <div className='space-y-3'>
                {analysis.step_by_step_guide.map((step: DebugStep, index: number) => (
                  <div key={index} className='bg-white rounded-lg p-3 flex items-start gap-3 border border-yellow-200'>
                    <div className='bg-yellow-500 text-white w-7 h-7 rounded-full flex items-center justify-center font-bold text-sm flex-shrink-0'>
                      {step.step}
                    </div>
                    <div className='flex-1'>
                      <p className='font-medium text-gray-800'>{step.action}</p>
                      <p className='text-sm text-gray-600 mt-1'>{step.detail}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* 修正提案 */}
          {analysis.fix_suggestions && analysis.fix_suggestions.length > 0 && (
            <div className='bg-gradient-to-br from-green-50 to-emerald-50 border-2 border-green-200 rounded-xl p-5 shadow-lg'>
              <h3 className='font-bold text-green-800 text-lg mb-3 flex items-center gap-2'>
                <span className='text-xl'>🔧</span>
                修正提案
              </h3>
              <ul className='space-y-2'>
                {analysis.fix_suggestions.map((suggestion: string, index: number) => (
                  <li key={index} className='bg-white rounded-lg p-3 flex items-start gap-2 border border-green-200'>
                    <span className='text-green-600 text-lg mt-0.5'>✓</span>
                    <span className='text-gray-700'>{suggestion}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* 類似例 */}
          {analysis.similar_examples && analysis.similar_examples.length > 0 && (
            <div className='bg-gradient-to-br from-indigo-50 to-blue-50 border-2 border-indigo-200 rounded-xl p-5 shadow-lg'>
              <h3 className='font-bold text-indigo-800 text-lg mb-3 flex items-center gap-2'>
                <span className='text-xl'>📝</span>
                コード例
              </h3>
              <div className='space-y-4'>
                {analysis.similar_examples.map((example: SimilarExample, index: number) => (
                  <div key={index} className='bg-white rounded-lg p-4 border border-indigo-200'>
                    <div className='grid md:grid-cols-2 gap-3'>
                      <div>
                        <p className='text-sm font-bold text-red-600 mb-1 flex items-center gap-1'>
                          <span>❌</span> 間違い
                        </p>
                        <pre className='bg-red-50 rounded p-2 text-sm font-mono overflow-x-auto'>{example.wrong}</pre>
                      </div>
                      <div>
                        <p className='text-sm font-bold text-green-600 mb-1 flex items-center gap-1'>
                          <span>✅</span> 正しい
                        </p>
                        <pre className='bg-green-50 rounded p-2 text-sm font-mono overflow-x-auto'>
                          {example.correct}
                        </pre>
                      </div>
                    </div>
                    <p className='text-sm text-gray-600 mt-2 bg-gray-50 rounded p-2'>{example.explanation}</p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* 学習リソース */}
          {analysis.learning_resources && analysis.learning_resources.length > 0 && (
            <div className='bg-gradient-to-br from-teal-50 to-cyan-50 border-2 border-teal-200 rounded-xl p-5 shadow-lg'>
              <h3 className='font-bold text-teal-800 text-lg mb-3 flex items-center gap-2'>
                <span className='text-xl'>📖</span>
                もっと学ぶ
              </h3>
              <ul className='space-y-2'>
                {analysis.learning_resources.map((resource: string, index: number) => (
                  <li key={index} className='bg-white rounded-lg p-3 border border-teal-200'>
                    <span className='text-gray-700 flex items-center gap-2'>
                      <span className='text-teal-500'>📌</span>
                      {resource}
                    </span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* コンテキスト情報 */}
          {analysis.context?.problematic_line && (
            <div className='bg-gray-50 border-2 border-gray-200 rounded-xl p-5 shadow-lg'>
              <h3 className='font-bold text-gray-800 text-lg mb-3 flex items-center gap-2'>
                <span className='text-xl'>📍</span>
                問題のコード
              </h3>
              <pre className='bg-white rounded-lg p-4 text-sm font-mono overflow-x-auto border border-gray-300'>
                <code className='text-red-600'>{analysis.context.problematic_line}</code>
              </pre>
              {analysis.context.surrounding_lines && analysis.context.surrounding_lines.length > 0 && (
                <details className='mt-3'>
                  <summary className='cursor-pointer text-sm text-gray-600 hover:text-gray-800'>
                    前後のコードを表示...
                  </summary>
                  <pre className='bg-white rounded-lg p-4 text-sm font-mono overflow-x-auto border border-gray-300 mt-2'>
                    {analysis.context.surrounding_lines.join('\n')}
                  </pre>
                </details>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  )
}
