import { cookies } from "next/headers";
import { redirect } from "next/navigation";
import { HomeHeader } from "@/components/home/HomeHeader";
import { HeroSection } from "@/components/home/HeroSection";
import { ProblemSection } from "@/components/home/ProblemSection";
import { SolutionSection } from "@/components/home/SolutionSection";
import { HowItWorksSection } from "@/components/home/HowItWorksSection";
import { AccessibilitySection } from "@/components/home/AccessibilitySection";
import { FinalCtaSection } from "@/components/home/FinalCtaSection";

export const metadata = {
  title: "em círculo — organize sua rede de apoio",
  description:
    "A Em Círculo ajuda familiares, cuidadores e pessoas de apoio a compartilhar tarefas, medicamentos e informações, reduzindo a sobrecarga de quem coordena o cuidado.",
};

export default async function HomePage() {
  const cookieStore = await cookies();
  const token = cookieStore.get("cc_access_token")?.value;

  // Authenticated users go directly to the dashboard flow
  if (token) {
    redirect("/dashboard");
  }

  return (
    <>
      <HomeHeader />
      <HeroSection />
      <ProblemSection />
      <SolutionSection />
      <HowItWorksSection />
      <AccessibilitySection />
      <FinalCtaSection />
    </>
  );
}
