// Typings para uso no Frontend e Server Actions (TypeScript)

export enum NotificationType {
  DOSE_REGISTERED = "DOSE_REGISTERED",
  TASK_CREATED = "TASK_CREATED",
  TASK_COMPLETED = "TASK_COMPLETED",
  STOCK_ALERT = "STOCK_ALERT",
  DOSE_ATRASADA = "DOSE_ATRASADA",
}

export interface NotificationResponse {
  id: string; // UUID
  care_group_id: string; // UUID
  title: string;
  message: string;
  type: NotificationType;
  is_read: boolean;
  created_at: string; // ISO 8601 DateTime
}

export interface MarkAsReadResponse {
  status: string;
}
