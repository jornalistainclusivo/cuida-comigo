"use client";

import { useState } from "react";
import type { CareGroup, CareGroupMember, CareRecipient } from "@/types";
import styles from "./CareGroupPanel.module.css";
import { updateCareGroupAction, deleteCareGroupAction, updateCareRecipientAction, deleteCareRecipientAction } from "../app/actions";
import { EditFormModal } from "./EditFormModal";

interface CareGroupPanelProps {
  group: CareGroup;
  recipient: CareRecipient | null;
  members: CareGroupMember[];
  userNames: Record<string, string>;
}

export function CareGroupPanel({
  group,
  recipient,
  members,
  userNames,
}: CareGroupPanelProps) {
  const [editingGroup, setEditingGroup] = useState<CareGroup | null>(null);
  const [deletingGroupId, setDeletingGroupId] = useState<string | null>(null);
  const [deletingGroupName, setDeletingGroupName] = useState("");

  const [editingRecipient, setEditingRecipient] = useState<CareRecipient | null>(null);
  const [deletingRecipientId, setDeletingRecipientId] = useState<string | null>(null);
  const [deletingRecipientName, setDeletingRecipientName] = useState("");

  const headingId = `group-heading-${group.id}`;
  const recipientHeadingId = `recipient-heading-${group.id}`;
  const membersHeadingId = `members-heading-${group.id}`;

  return (
    <section aria-labelledby={headingId} className={styles.panel}>
      <header className={styles.header}>
        <div style={{ display: "flex", alignItems: "center", gap: "var(--space-3)", flexWrap: "wrap" }}>
          <h2 id={headingId} style={{ margin: 0 }}>{group.name}</h2>
          <div style={{ display: "flex", gap: "var(--space-1)" }}>
            <button
              type="button"
              className="btn btn--secondary"
              style={{ padding: "var(--space-1) var(--space-2)", fontSize: "0.8rem", minHeight: "auto", border: "1px solid var(--color-border)" }}
              onClick={() => setEditingGroup(group)}
              aria-label={`Editar Grupo: ${group.name}`}
            >
              ✏️
            </button>
            <button
              type="button"
              className="btn btn--danger"
              style={{ padding: "var(--space-1) var(--space-2)", fontSize: "0.8rem", minHeight: "auto", backgroundColor: "var(--color-danger)", color: "#fff" }}
              onClick={() => {
                setDeletingGroupId(group.id);
                setDeletingGroupName(group.name);
              }}
              aria-label={`Excluir Grupo: ${group.name}`}
            >
              🗑️
            </button>
          </div>
        </div>
        <time
          dateTime={group.created_at}
          className={styles.meta}
          aria-label={`Grupo criado em ${formatDateForScreen(group.created_at)}`}
        >
          Criado em {formatDateForScreen(group.created_at)}
        </time>
      </header>

      {/* Care Recipient */}
      {recipient ? (
        <article
          aria-labelledby={recipientHeadingId}
          className={styles.recipientCard}
        >
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "var(--space-3)", flexWrap: "wrap" }}>
            <h3 id={recipientHeadingId} style={{ margin: 0 }}>Pessoa Cuidada</h3>
            <div style={{ display: "flex", gap: "var(--space-1)" }}>
              <button
                type="button"
                className="btn btn--secondary"
                style={{ padding: "var(--space-1) var(--space-2)", fontSize: "0.8rem", minHeight: "auto", border: "1px solid var(--color-border)" }}
                onClick={() => setEditingRecipient(recipient)}
                aria-label={`Editar Paciente: ${recipient.name}`}
              >
                ✏️
              </button>
              <button
                type="button"
                className="btn btn--danger"
                style={{ padding: "var(--space-1) var(--space-2)", fontSize: "0.8rem", minHeight: "auto", backgroundColor: "var(--color-danger)", color: "#fff" }}
                onClick={() => {
                  setDeletingRecipientId(recipient.id);
                  setDeletingRecipientName(recipient.name);
                }}
                aria-label={`Excluir Paciente: ${recipient.name}`}
              >
                🗑️
              </button>
            </div>
          </div>
          <dl className={styles.detailList}>
            <dt>Nome</dt>
            <dd>{recipient.name}</dd>

            {recipient.blood_type && (
              <>
                <dt>Tipo Sanguíneo</dt>
                <dd>{recipient.blood_type}</dd>
              </>
            )}

            {recipient.allergies.length > 0 && (
              <>
                <dt>Alergias</dt>
                <dd>
                  <ul aria-label="Lista de alergias">
                    {recipient.allergies.map((allergy) => (
                      <li key={allergy}>{allergy}</li>
                    ))}
                  </ul>
                </dd>
              </>
            )}
          </dl>
        </article>
      ) : (
        <p className={styles.empty} role="status">
          Nenhuma pessoa cuidada cadastrada neste grupo.
        </p>
      )}

      {/* Members */}
      <section aria-labelledby={membersHeadingId} className={styles.members}>
        <h3 id={membersHeadingId}>
          Membros
          <span className="visually-hidden">
            ({members.length} {members.length === 1 ? "membro" : "membros"})
          </span>
        </h3>

        {members.length > 0 ? (
          <ul aria-label="Lista de membros do grupo">
            {members.map((member) => {
              const name = userNames[member.user_id] || "Usuário Desconhecido";
              return (
                <li key={member.id} className={styles.memberItem} style={{ display: "flex", alignItems: "center", gap: "var(--space-3)", marginBottom: "var(--space-2)" }}>
                  <div 
                    aria-hidden="true" 
                    style={{ 
                      width: "40px", height: "40px", borderRadius: "var(--radius-full)", 
                      backgroundColor: "var(--color-primary-light)", color: "var(--color-primary)",
                      display: "flex", alignItems: "center", justifyContent: "center", 
                      fontWeight: "var(--font-weight-bold)", fontSize: "var(--font-size-sm)"
                    }}
                  >
                    {getInitials(name)}
                  </div>
                  <div style={{ flex: 1 }}>
                    <span style={{ display: "block", fontWeight: "var(--font-weight-medium)" }}>{name}</span>
                  </div>
                  <span
                    className={`badge ${member.role === "ADMIN" ? "badge--claimed" : "badge--pending"}`}
                    aria-label={`Função: ${member.role === "ADMIN" ? "Administrador" : "Apoio"}`}
                  >
                    {member.role === "ADMIN" ? "Admin" : "Apoio"}
                  </span>
                </li>
              );
            })}
          </ul>
        ) : (
          <p role="status">Nenhum membro neste grupo.</p>
        )}
      </section>

      {editingGroup && (
        <EditFormModal
          title="Editar Grupo de Cuidado"
          type="group"
          initialData={editingGroup}
          onClose={() => setEditingGroup(null)}
          onSubmitAction={updateCareGroupAction.bind(null, editingGroup.id)}
        />
      )}

      {deletingGroupId && (
        <EditFormModal
          title={`Excluir Grupo: ${deletingGroupName}`}
          type="delete_confirm"
          onClose={() => {
            setDeletingGroupId(null);
            setDeletingGroupName("");
          }}
          onDeleteAction={() => deleteCareGroupAction(deletingGroupId)}
        />
      )}

      {editingRecipient && (
        <EditFormModal
          title="Editar Paciente"
          type="recipient"
          initialData={editingRecipient}
          onClose={() => setEditingRecipient(null)}
          onSubmitAction={updateCareRecipientAction.bind(null, editingRecipient.id)}
        />
      )}

      {deletingRecipientId && (
        <EditFormModal
          title={`Excluir Paciente: ${deletingRecipientName}`}
          type="delete_confirm"
          onClose={() => {
            setDeletingRecipientId(null);
            setDeletingRecipientName("");
          }}
          onDeleteAction={() => deleteCareRecipientAction(deletingRecipientId)}
        />
      )}
    </section>
  );
}

/**
 * Formats an ISO 8601 datetime for human-readable screen display
 * using the browser's Intl.DateTimeFormat API.
 */
function formatDateForScreen(isoDate: string): string {
  return new Intl.DateTimeFormat("pt-BR", {
    dateStyle: "long",
    timeStyle: "short",
    timeZone: "America/Sao_Paulo",
  }).format(new Date(isoDate));
}

function getInitials(name: string): string {
  const parts = name.trim().split(/\s+/);
  if (parts.length >= 2) {
    return (parts[0][0] + parts[1][0]).toUpperCase();
  }
  return name.slice(0, 2).toUpperCase();
}
