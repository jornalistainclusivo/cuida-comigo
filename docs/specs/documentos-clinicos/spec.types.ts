/**
 * @spec-source docs/specs/documentos-clinicos/spec.md
 * @generated 2026-07-12
 */

/**
 * Representa os campos de texto do Multipart/FormData para upload.
 * O arquivo binário irá em um campo 'file'.
 */
export interface DocumentCreate {
  title: string;
  document_type: "RECEITA" | "LAUDO" | "EXAME" | "OUTROS";
}

/**
 * Resposta de Metadados do Documento (Usado na listagem GET)
 */
export interface DocumentResponse {
  id: string;
  care_recipient_id: string;
  title: string;
  document_type: "RECEITA" | "LAUDO" | "EXAME" | "OUTROS";
  uploaded_at: string; // ISO 8601
  uploaded_by_id: string; // ID do membro que fez o upload
}

/**
 * Resposta para a requisição de download seguro
 */
export interface PresignedUrlResponse {
  url: string; // Presigned URL
  expires_in: number; // Em segundos (Ex: 300)
}
