import { useState, useEffect } from "react";
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

// TypeScript interface for backend data
interface HealthData {
  current_metrics: {
    heart_rate: number;
    blood_oxygen: number;
    temperature: number;
    respiration_rate: number;
    health_score: number;
    steps?: number;
  };
  status: {
    anomaly: string;
    risk_level: string;
  };
  statistics: {
    total_records: number;
    anomaly_count: number;
    avg_health_score: number;
  };
  trends: {
    heart_rate: number[];
    blood_oxygen: number[];
    temperature: number[];
  };
}

const Index = () => {
  const [healthData, setHealthData] = useState<HealthData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Listen for health data updates from backend
    const handleHealthDataUpdate = (event: CustomEvent) => {
      setHealthData(event.detail);
      setLoading(false);
    };

    const handleHealthDataError = (event: CustomEvent) => {
      setError(event.detail);
      setLoading(false);
    };

    window.addEventListener('healthDataUpdated', handleHealthDataUpdate as EventListener);
    window.addEventListener('healthDataError', handleHealthDataError as EventListener);

    // Check if data is already loaded
    if (window.healthAPI && window.healthAPI.getCurrentData()) {
      setHealthData(window.healthAPI.getCurrentData());
      setLoading(false);
    }

    return () => {
      window.removeEventListener('healthDataUpdated', handleHealthDataUpdate as EventListener);
      window.removeEventListener('healthDataError', handleHealthDataError as EventListener);
    };
  }, []);

  // Calculate derived values
  const heartRate = healthData?.current_metrics.heart_rate || 124;
  const bloodOxygen = healthData?.current_metrics.blood_oxygen || 102;
  const temperature = healthData?.current_metrics.temperature || 37.1;
  const respirationRate = healthData?.current_metrics.respiration_rate || 16;
  const healthScore = healthData?.current_metrics.health_score || 85;
  const steps = healthData?.current_metrics.steps || Math.floor(healthScore * 100);

  // Calculate BMI-like weight metric (simulated)
  const weight = 72 + (Math.random() * 4 - 2);
  const calories = Math.floor(1800 + Math.random() * 400);

  // Status checks
  const isHeartNormal = heartRate >= 60 && heartRate <= 100;
  const isLungsNormal = respirationRate >= 12 && respirationRate <= 20;

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-muted-foreground">Loading health data...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center p-6">
        <div className="glass-card rounded-3xl p-8 max-w-md text-center">
          <div className="text-4xl mb-4">⚠️</div>
          <h2 className="text-xl font-bold mb-2">Error Loading Data</h2>
          <p className="text-muted-foreground mb-4">{error}</p>
          <button
            onClick={() => {
              setLoading(true);
              setError(null);
              window.healthAPI?.fetchData();
            }}
            className="px-6 py-2 bg-primary text-white rounded-lg hover:bg-primary/90 transition-colors"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen p-6 md:p-8 lg:p-12">
      <div className="max-w-[1400px] mx-auto space-y-6">
        {/* Header with status */}
        <div className="glass-card rounded-3xl p-6">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-2xl font-bold">AI Health Dashboard</h1>
              <p className="text-sm text-muted-foreground">
                Status: {healthData?.status.anomaly || "Normal"} | Risk: {healthData?.status.risk_level || "Low Risk"}
              </p>
            </div>
            <div className="text-right">
              <div className="text-3xl font-bold">{healthScore}</div>
              <div className="text-xs text-muted-foreground">Health Score</div>
            </div>
          </div>
        </div>

        {/* Top row - Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <MetricCard
            title="Weight"
            subtitle="Lost 0.4kg"
            value={weight.toFixed(1)}
            unit="kg"
            chartData={healthData?.trends.heart_rate.slice(0, 12) || [45, 52, 48, 65, 42, 58, 63, 48, 55, 52, 48, 45]}
          />
          <MetricCard
            title="Food"
            subtitle={`${calories}/1,800 kCal`}
            value={calories.toString()}
            unit="kcal"
            chartData={healthData?.trends.blood_oxygen.slice(0, 12) || [35, 42, 38, 55, 32, 48, 53, 38, 45, 42, 38, 35]}
          />
        </div>

        {/* Middle section - Steps, Heart, Body */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <StepsCircle current={steps} goal={10000} />
          <HeartRateCard bpm={heartRate} />
          <BodyDiagramCard />
        </div>

        {/* Bottom section - Organs and Vitals */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6">
          <OrganCard
            title="Heart"
            status={isHeartNormal ? "Normal" : "Warning"}
            image={heartImage}
          />
          <OrganCard
            title="Lungs"
            status={isLungsNormal ? "Normal" : "Warning"}
            image={lungsImage}
          />
          <VitalSignCard
            icon={<Droplet className="w-5 h-5" />}
            title="Blood Status"
            subtitle={`${bloodOxygen}/70`}
            value={bloodOxygen.toString()}
            chart={
              <div className="flex items-end gap-0.5 h-16">
                {(healthData?.trends.blood_oxygen.slice(0, 12) || [40, 65, 45, 70, 50, 75, 55, 80, 60, 85, 70, 75]).map((height, idx) => (
                  <div
                    key={idx}
                    className="flex-1 bg-muted rounded-sm"
                    style={{ height: `${(height / 100) * 100}%` }}
                  />
                ))}
              </div>
            }
          />
          <VitalSignCard
            icon={<Thermometer className="w-5 h-5" />}
            title="Temperature"
            subtitle={temperature.toFixed(1)}
            value={`${temperature.toFixed(1)}°`}
            chart={
              <svg className="w-full h-16" viewBox="0 0 200 60">
                <polyline
                  points={healthData?.trends.temperature.slice(0, 10).map((temp, idx) => 
                    `${idx * 20},${60 - ((temp - 35) / 5 * 60)}`
                  ).join(' ') || "0,40 20,38 40,35 60,30 80,32 100,28 120,30 140,25 160,27 180,24 200,26"}
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
            subtitle={`${heartRate} bpm`}
            value={heartRate.toString()}
            chart={
              <svg className="w-full h-16" viewBox="0 0 200 60">
                <polyline
                  points={healthData?.trends.heart_rate.slice(0, 15).map((hr, idx) => {
                    const x = idx * 13;
                    const normalizedHR = ((hr - 60) / 100) * 40 + 30;
                    return `${x},${60 - normalizedHR}`;
                  }).join(' ') || "0,30 30,30 35,10 40,50 45,30 70,30 75,10 80,50 85,30 115,30 120,10 125,50 130,30 160,30 165,10 170,50 175,30 200,30"}
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
          
          {/* AI Insights */}
          {healthData && (
            <div className="glass-card rounded-3xl p-6 md:col-span-2">
              <h3 className="text-lg font-semibold mb-4">📊 Health Statistics</h3>
              <div className="grid grid-cols-3 gap-4">
                <div>
                  <div className="text-2xl font-bold">{healthData.statistics.total_records}</div>
                  <div className="text-xs text-muted-foreground">Total Records</div>
                </div>
                <div>
                  <div className="text-2xl font-bold text-destructive">{healthData.statistics.anomaly_count}</div>
                  <div className="text-xs text-muted-foreground">Anomalies</div>
                </div>
                <div>
                  <div className="text-2xl font-bold text-primary">{healthData.statistics.avg_health_score.toFixed(1)}</div>
                  <div className="text-xs text-muted-foreground">Avg Score</div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Index;
