"use client";

import { useState } from "react";
import styles from "../app/notificacoes/page.module.css";
import { Notification, markNotificationAsReadAction } from "@/app/actions/notifications";
import { useRouter } from "next/navigation";

export default function NotificationItem({
  notification,
}: {
  notification: Notification;
}) {
  const [isRead, setIsRead] = useState(notification.is_read);
  const [isLoading, setIsLoading] = useState(false);
  const router = useRouter();

  const handleMarkAsRead = async () => {
    if (isRead || isLoading) return;

    setIsLoading(true);
    try {
      const success = await markNotificationAsReadAction(notification.id);
      if (success) {
        setIsRead(true);
        router.refresh();
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <>
      {/* eslint-disable-next-line jsx-a11y/click-events-have-key-events, jsx-a11y/no-noninteractive-element-interactions */}
      <li
        className={`${styles.notificationItem} ${!isRead ? styles.unread : ""} ${
          isLoading ? styles.loading : ""
        }`}
        onClick={handleMarkAsRead}
        style={{ cursor: !isRead ? "pointer" : "default" }}
      >
      <div className={styles.icon}>
        {notification.type === "DOSE_REGISTERED" && "💊"}
        {notification.type === "TASK_CREATED" && "📋"}
        {notification.type === "TASK_COMPLETED" && "✅"}
        {notification.type === "STOCK_ALERT" && "⚠️"}
        {!["DOSE_REGISTERED", "TASK_CREATED", "TASK_COMPLETED", "STOCK_ALERT"].includes(
          notification.type
        ) && "🔔"}
      </div>
      <div className={styles.content}>
        <strong>{notification.title}</strong>
        <p>{notification.message}</p>
        <small>{new Date(notification.created_at).toLocaleString("pt-BR")}</small>
      </div>
    </li>
    </>
  );
}
