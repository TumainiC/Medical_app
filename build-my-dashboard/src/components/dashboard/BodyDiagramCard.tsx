import bodyImage from "@/assets/body-diagram.png";

export const BodyDiagramCard = () => {
  return (
    <div className="glass-card rounded-3xl p-8 h-full flex items-center justify-center">
      <div className="relative">
        <img 
          src={bodyImage} 
          alt="Body Diagram" 
          className="w-48 h-auto object-contain"
        />
        
        {/* Indicator dots */}
        <div className="absolute top-[15%] right-[45%] w-3 h-3 bg-accent rounded-full animate-pulse" />
        <div className="absolute top-[25%] right-[20%] w-3 h-3 bg-accent rounded-full animate-pulse" style={{ animationDelay: '0.5s' }} />
        <div className="absolute top-[65%] right-[40%] w-3 h-3 bg-accent rounded-full animate-pulse" style={{ animationDelay: '1s' }} />
      </div>
    </div>
  );
};
