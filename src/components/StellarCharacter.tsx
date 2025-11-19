import { motion } from "framer-motion";
import stellarChar from "@/assets/stellar-landingpage.svg";

const StellarCharacter = () => {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.8 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.8 }}
      className="relative w-full h-full flex items-center justify-center"
    >
      {/* Frame container with rounded border */}
      <div className="relative bg-card rounded-3xl border border-border shadow-lg hover:shadow-2xl transition-all duration-300 overflow-hidden w-full max-w-lg">
        <img
          src={stellarChar}
          alt="Stellecta Character"
          className="w-full h-auto object-contain drop-shadow-2xl"
        />
        
        {/* Glow effect inside frame */}
        <div className="absolute inset-0 bg-gradient-stellar opacity-20 blur-3xl rounded-3xl pointer-events-none" />
      </div>
    </motion.div>
  );
};

export default StellarCharacter;
