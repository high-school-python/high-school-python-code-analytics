'use client'

import Image from 'next/image'
import { useState } from 'react'
import AnalysisPanel from '@/components/AnalysisPanel'
import CodeEditor from '@/components/CodeEditor'
import ErrorAnalysisPanel from '@/components/ErrorAnalysisPanel'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import VisualizationPanel from '@/components/VisualizationPanel'

export default function Home() {
  const [code, setCode] = useState<string>('# Pythonコードをここに入力してください\n')
  const [activeTab, setActiveTab] = useState<string>('analysis')
  const [shouldAnalyze, setShouldAnalyze] = useState<boolean>(false)

  return (
    <div className='min-h-screen gradient-bg'>
      <header className='bg-white/80 backdrop-blur-sm shadow-lg border-b border-blue-100'>
        <div className='max-w-7xl mx-auto px-4 sm:px-6 lg:px-8'>
          <div className='py-4 flex items-center justify-between'>
            <div className='flex items-center gap-4'>
              <Image
                src='/Python_select_yoko.png'
                alt='ハイスクールPython'
                width={300}
                height={80}
                className='h-12 w-auto'
                priority
              />
              <div className='h-10 w-[1px] bg-gray-300' />
              <p className='text-sm font-medium text-gray-700'>コード解析ツール 💻 🐍</p>
            </div>
            <div className='hidden md:flex items-center gap-2 text-sm text-gray-600'>
              <span className='inline-flex items-center gap-1'>
                <span className='w-2 h-2 bg-green-400 rounded-full animate-pulse' />
                オンライン
              </span>
            </div>
          </div>
        </div>
      </header>

      <main className='max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8'>
        <div className='grid grid-cols-1 lg:grid-cols-2 gap-6'>
          {/* 左側: コードエディタ */}
          <div className='bg-white rounded-2xl shadow-lg panel-shadow transition-all duration-300'>
            <div className='p-4 border-b border-gray-100 bg-gradient-to-r from-blue-50 to-transparent rounded-t-2xl'>
              <h2 className='text-lg font-bold text-gray-800 flex items-center gap-2'>
                <span className='text-2xl'>📝</span>
                コードエディタ
              </h2>
            </div>
            <div className='p-6'>
              <CodeEditor value={code} onChange={setCode} />
              <button
                type='button'
                onClick={() => setShouldAnalyze(true)}
                disabled={activeTab === 'error'}
                className={`mt-4 w-full py-3 px-6 rounded-xl font-bold text-lg transition-all duration-300 flex items-center justify-center gap-2 ${
                  activeTab === 'error' ? 'bg-gray-300 text-gray-500 cursor-not-allowed' : 'btn-primary text-white'
                }`}
              >
                <span className='text-xl'>✨</span>
                コードを解析する
              </button>
            </div>
          </div>

          {/* 右側: 解析結果 */}
          <div className='bg-white rounded-2xl shadow-lg panel-shadow transition-all duration-300'>
            <div className='p-4 border-b border-gray-100 bg-gradient-to-r from-blue-50 to-transparent rounded-t-2xl'>
              <h2 className='text-lg font-bold text-gray-800 flex items-center gap-2'>
                <span className='text-2xl'>📈</span>
                解析結果
              </h2>
            </div>
            <div className='p-6'>
              <Tabs value={activeTab} onValueChange={setActiveTab}>
                <TabsList className='grid w-full grid-cols-4 mb-4 bg-blue-50/50 p-1 rounded-xl'>
                  <TabsTrigger
                    value='analysis'
                    className='data-[state=active]:bg-white data-[state=active]:shadow-md rounded-lg transition-all duration-200 font-medium'
                  >
                    <span className='flex items-center gap-1'>
                      <span className='text-lg'>🔍</span>
                      コードを解析する
                    </span>
                  </TabsTrigger>
                  <TabsTrigger
                    value='visualization'
                    className='data-[state=active]:bg-white data-[state=active]:shadow-md rounded-lg transition-all duration-200 font-medium'
                  >
                    <span className='flex items-center gap-1'>
                      <span className='text-lg'>🎨</span>
                      ビジュアルで見る
                    </span>
                  </TabsTrigger>
                  <TabsTrigger
                    value='error'
                    className='data-[state=active]:bg-white data-[state=active]:shadow-md rounded-lg transition-all duration-200 font-medium'
                  >
                    <span className='flex items-center gap-1'>
                      <span className='text-lg'>🚨</span>
                      エラーを解析する
                    </span>
                  </TabsTrigger>
                </TabsList>

                <TabsContent value='analysis'>
                  <AnalysisPanel
                    code={code}
                    shouldAnalyze={shouldAnalyze}
                    onAnalyzeComplete={() => setShouldAnalyze(false)}
                  />
                </TabsContent>

                <TabsContent value='visualization'>
                  <VisualizationPanel
                    code={code}
                    shouldAnalyze={shouldAnalyze}
                    onAnalyzeComplete={() => setShouldAnalyze(false)}
                  />
                </TabsContent>

                <TabsContent value='error'>
                  <ErrorAnalysisPanel
                    code={code}
                    shouldAnalyze={shouldAnalyze}
                    onAnalyzeComplete={() => setShouldAnalyze(false)}
                  />
                </TabsContent>
              </Tabs>
            </div>
          </div>
        </div>
      </main>

      <footer className='bg-white/80 backdrop-blur-sm border-t border-blue-100 mt-12'>
        <div className='max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6'>
          <div className='flex flex-col items-center gap-2'>
            <p className='text-sm text-gray-600'>
              © {new Date().getFullYear()} ハイスクールPython. All rights reserved.
            </p>
            <a
              href='https://high-school-python.jp/'
              target='_blank'
              rel='noopener noreferrer'
              className='text-sm text-blue-600 hover:text-blue-800 font-medium flex items-center gap-1 group'
            >
              <span>ハイスクールPython 公式サイト</span>
              <span className='group-hover:translate-x-1 transition-transform'>→</span>
            </a>
          </div>
        </div>
      </footer>
    </div>
  )
}
