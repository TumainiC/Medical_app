import { MetricCard } from "@/components/dashboard/MetricCard";
import { StepsCircle } from "@/components/dashboard/StepsCircle";
import { HeartRateCard } from "@/components/dashboard/HeartRateCard";
import { OrganCard } from "@/components/dashboard/OrganCard";
import { VitalSignCard } from "@/components/dashboard/VitalSignCard";
import { BodyDiagramCard } from "@/components/dashboard/BodyDiagramCard";
import { SleepCard } from "@/components/dashboard/SleepCard";
import { Activity, Droplet, Thermometer } from "lucide-react";
import heartImage from "@/assets/heart-3d.png";
import lungsImage from "@/assets/lungs-3d.png";

const Index = () => {
  return (
    <div className="min-h-screen p-6 md:p-8 lg:p-12">
      <div className="max-w-[1400px] mx-auto space-y-6">
        {/* Top row - Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <MetricCard
            title="Weight"
            subtitle="Lost 0.4kg"
            value="74.2"
            unit="kg"
            chartData={[45, 52, 48, 65, 42, 58, 63, 48, 55, 52, 48, 45]}
          />
          <MetricCard
            title="Food"
            subtitle="254/1,342 kCal"
            value="253"
            unit="kcal"
            chartData={[35, 42, 38, 55, 32, 48, 53, 38, 45, 42, 38, 35]}
          />
        </div>

        {/* Middle section - Steps, Heart, Body */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <StepsCircle current={7425} goal={10000} />
          <HeartRateCard bpm={124} />
          <BodyDiagramCard />
        </div>

        {/* Bottom section - Organs and Vitals */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6">
          <OrganCard
            title="Heart"
            status="Normal"
            image={heartImage}
          />
          <OrganCard
            title="Lungs"
            status="Normal"
            image={lungsImage}
          />
          <VitalSignCard
            icon={<Droplet className="w-5 h-5" />}
            title="Blood Status"
            subtitle="102/70"
            value="102"
            chart={
              <div className="flex items-end gap-0.5 h-16">
                {[40, 65, 45, 70, 50, 75, 55, 80, 60, 85, 70, 75].map((height, idx) => (
                  <div
                    key={idx}
                    className="flex-1 bg-muted rounded-sm"
                    style={{ height: `${height}%` }}
                  />
                ))}
              </div>
            }
          />
          <VitalSignCard
            icon={<Thermometer className="w-5 h-5" />}
            title="Temperature"
            subtitle="37.1"
            value="37.1°"
            chart={
              <svg className="w-full h-16" viewBox="0 0 200 60">
                <polyline
                  points="0,40 20,38 40,35 60,30 80,32 100,28 120,30 140,25 160,27 180,24 200,26"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  className="text-primary"
                />
              </svg>
            }
          />
          <VitalSignCard
            icon={<Activity className="w-5 h-5" />}
            title="Heart Rate"
            subtitle="124 bpm"
            value="124"
            chart={
              <svg className="w-full h-16" viewBox="0 0 200 60">
                <polyline
                  points="0,30 30,30 35,10 40,50 45,30 70,30 75,10 80,50 85,30 115,30 120,10 125,50 130,30 160,30 165,10 170,50 175,30 200,30"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  className="text-accent"
                />
              </svg>
            }
          />
        </div>

        {/* Sleep tracking */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <SleepCard
            hours={7}
            minutes={30}
            startTime="00:30"
            endTime="08:00"
          />
        </div>
      </div>
    </div>
  );
};

export default Index;
