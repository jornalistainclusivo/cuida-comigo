import { MedicationPanel } from "@/components/MedicationPanel";
import type { MedicationProtocol } from "@/types";
import styles from "./page.module.css";
import { logMedicationAction } from "../actions";

async function fetchProtocols(): Promise<MedicationProtocol[]> {
  try {
    const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || process.env.API_BASE_URL || "http://127.0.0.1:8000";
    const recipient_id = "b2c3d4e5-f6a7-8901-bcde-f12345678901"; // Mock recipient ID
    const res = await fetch(`${API_BASE_URL}/api/v1/care-recipients/${recipient_id}/protocols`, { cache: "no-store" });
    if (res.ok) {
      return (await res.json()) as MedicationProtocol[];
    }
    console.error("Erro na resposta do FastAPI ao buscar protocolos:", res.status);
  } catch (error) {
    console.error("FastAPI indisponível. Erro ao buscar protocolos reais:", error);
  }
  return []; // Removed DEMO_PROTOCOLS fallback
}

export default async function MedicamentosPage() {
  const protocols = await fetchProtocols();

  return (
    <article className={styles.container}>
      <header className={styles.pageHeader}>
        <h1>Farmácia</h1>
        <p>
          Controle os medicamentos, registre doses administradas e monitore o estoque da sua família.
        </p>
      </header>
      
      <MedicationPanel protocols={protocols} onLogMedication={logMedicationAction} />
    </article>
  );
}
