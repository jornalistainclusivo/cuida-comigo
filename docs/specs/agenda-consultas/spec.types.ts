/**
 * @spec-source docs/specs/agenda-consultas/spec.md
 * @generated 2026-07-11 — DO NOT EDIT MANUALLY
 * @prd-coverage FR-001
 *
 * ⚠️  Source of truth is spec.md. Edit there, then regenerate this file.
 */

/**
 * DTO para Criação de Consulta Médica (Request)
 */
export interface AppointmentCreate {
  /** 
   * Título descritivo do agendamento (Ex: Consulta Cardiologista) 
   */
  title: string;
  
  /** 
   * Data e hora do agendamento em ISO-8601 UTC
   * Exemplo: "2026-07-20T14:30:00Z"
   */
  scheduled_at: string;
  
  /** 
   * Nome do profissional ou especialista
   */
  provider_name?: string;
  
  /** 
   * Local do atendimento
   */
  location?: string;
}

/**
 * DTO para Resposta de Consulta Médica (Response)
 */
export interface AppointmentResponse {
  id: string;
  care_recipient_id: string;
  title: string;
  scheduled_at: string;
  provider_name: string | null;
  location: string | null;
  created_at: string;
}
