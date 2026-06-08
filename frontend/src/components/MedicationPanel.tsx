"use client";

import { useState } from "react";
import type { MedicationProtocol } from "@/types";
import styles from "./MedicationPanel.module.css";

interface MedicationPanelProps {
  protocols: MedicationProtocol[];
  onLogMedication: (protocolId: string) => Promise<{ success: boolean; stock_alert?: boolean; remaining_balance?: number; error?: string } | void>;
}

export function MedicationPanel({ protocols, onLogMedication }: MedicationPanelProps) {
  const [selectedProtocolId, setSelectedProtocolId] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [toastMessage, setToastMessage] = useState<string | null>(null);

  const handleOpenConfirm = (protocolId: string) => {
    setSelectedProtocolId(protocolId);
  };

  const handleCloseConfirm = () => {
    setSelectedProtocolId(null);
  };

  const handleConfirmDose = async (protocolId: string) => {
    setIsSubmitting(true);
    try {
      const result = await onLogMedication(protocolId);
      setSelectedProtocolId(null);

      if (result && result.success && result.stock_alert) {
        setToastMessage(`Atenção: O estoque crítico foi atingido (${result.remaining_balance} restantes). Uma tarefa de reposição foi gerada.`);
        setTimeout(() => setToastMessage(null), 8000);
      }
    } catch (error) {
      console.error("Falha ao registrar dose", error);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <section className={styles.panel}>
      <h2>Meus Medicamentos</h2>
      
      {toastMessage && (
        <div className={styles.toast} role="alert" aria-live="assertive">
          {toastMessage}
          <button className={styles.toastClose} onClick={() => setToastMessage(null)} aria-label="Fechar alerta">&times;</button>
        </div>
      )}

      {protocols.length === 0 ? (
        <p className={styles.emptyState}>Nenhum medicamento cadastrado.</p>
      ) : (
        <div className={styles.list}>
          {protocols.map((protocol) => {
            const isLowStock = protocol.stock_count <= protocol.safety_threshold;
            const isConfirming = selectedProtocolId === protocol.id;

            return (
              <div 
                key={protocol.id} 
                className={`${styles.card} ${isLowStock ? styles.cardLowStock : ''}`}
              >
                <div className={styles.cardHeader}>
                  <div className={styles.info}>
                    <h3 className={styles.name}>{protocol.medication_name}</h3>
                    <p className={styles.details}>
                      {protocol.dosage} • A cada {protocol.frequency_interval_hours}h
                    </p>
                  </div>
                  <div className={styles.stock}>
                    <span className={styles.stockLabel}>Estoque</span>
                    <strong className={styles.stockCount}>{protocol.stock_count} un.</strong>
                  </div>
                </div>

                <div className={styles.actions}>
                  <button 
                    className={styles.logButton}
                    onClick={() => handleOpenConfirm(protocol.id)}
                    aria-expanded={isConfirming}
                    aria-controls={`confirm-panel-${protocol.id}`}
                  >
                    Registrar Dose
                  </button>
                </div>

                {isConfirming && (
                  <div 
                    id={`confirm-panel-${protocol.id}`}
                    className={styles.confirmPanel}
                    role="region"
                    aria-label="Confirmar administração de dose"
                  >
                    <p>Tem certeza que deseja registrar a administração desta dose?</p>
                    <div className={styles.confirmActions}>
                      <button 
                        className={styles.cancelButton}
                        onClick={handleCloseConfirm}
                        disabled={isSubmitting}
                      >
                        Cancelar
                      </button>
                      <button 
                        className={styles.submitButton}
                        onClick={() => handleConfirmDose(protocol.id)}
                        disabled={isSubmitting}
                      >
                        {isSubmitting ? "Registrando..." : "Confirmar Dose"}
                      </button>
                    </div>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}
    </section>
  );
}
