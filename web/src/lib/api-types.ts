// API Response Types

export interface AnalyzeResponse {
  success: boolean
  error?: string | null
  message?: string | null
  line?: number | null
  offset?: number | null
  text?: string | null
  structure?: Record<string, unknown> | null
  style_issues?: StyleIssue[] | null
  improvements?: Improvement[] | null
  stats?: Stats | null
  summary?: Summary | null
}

export interface StyleIssue {
  line: number
  type: string
  message: string
  severity?: string
}

export interface Improvement {
  type: string
  message: string
  line?: number
}

export interface Stats {
  total_lines: number
  code_lines: number
  import_count: number
  function_count: number
  class_count: number
  complexity_score: number
}

export interface Summary {
  description: string
  main_concepts: string[]
  difficulty: string
  quality_score?: number
  total_issues?: number
  total_suggestions?: number
}

export interface VisualizeResponse {
  success: boolean
  steps: SimulatedStep[]
  structure: Record<string, unknown>
  flow_diagram: string
  explanation: string
  error?: string | null
  flowchart?: string
  explanations?: StepExplanation[]
  message?: string | null
}

export interface SimulatedStep {
  line_number: number
  code: string
  action: string
  description: string
  scope: string
  line?: number // alias for line_number
  variables?: Record<string, unknown>
}

export interface StepExplanation {
  line: number
  explanation: string
}

export interface ErrorAnalyzeResponse {
  success: boolean
  error_type: string
  line_number: number
  column_number: number
  simple_explanation: string
  detailed_explanation: string
  common_causes: string[]
  fix_suggestions: string[]
  similar_examples: SimilarExample[]
  learning_resources: string[]
  step_by_step_guide?: DebugStep[]
  preventive_tips?: string[]
  context?: ErrorContext
  difficulty_level?: number
  concept_explanation?: string
  visual_explanation?: {
    content: string
  }
}

export interface SimilarExample {
  wrong: string
  correct: string
  explanation: string
}

export interface DebugStep {
  step: number
  action: string
  detail: string
}

export interface ErrorContext {
  problematic_line?: string
  line_before?: string
  line_after?: string
  surrounding_lines?: string[]
}
