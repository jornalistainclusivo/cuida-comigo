import { getMyGroupIdAction, getNotificationsAction } from "@/app/actions/notifications";
import NotificationItem from "@/components/NotificationItem";
import styles from "./page.module.css";
import Link from "next/link";

export default async function NotificacoesPage() {
  const groupId = await getMyGroupIdAction();
  
  if (!groupId) {
    return (
      <div className={styles.container}>
        <h1>Notificações</h1>
        <p>Você precisa estar em um grupo de cuidado para ver as notificações.</p>
        <Link href="/" className={styles.backLink}>Voltar para o Painel</Link>
      </div>
    );
  }

  // Busca notificações (ignora cache para ter dados frescos)
  // eslint-disable-next-line react-hooks/purity
  const notifications = await getNotificationsAction(groupId, false, Date.now());

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h1>Notificações</h1>
        <Link href="/" className={styles.backLink}>Voltar para o Painel</Link>
      </div>

      {notifications.length === 0 ? (
        <div className={styles.emptyState}>
          <p>Nenhuma notificação nova por aqui.</p>
        </div>
      ) : (
        <ul className={styles.notificationList}>
          {notifications.map((n) => (
            <NotificationItem key={n.id} notification={n} />
          ))}
        </ul>
      )}
    </div>
  );
}
