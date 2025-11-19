import { motion } from "framer-motion";
import { BrainCircuit, ShieldCheck, Gem } from "lucide-react";

const ThreePillars = () => {
  const pillars = [
    {
      icon: BrainCircuit,
      title: "Learn",
      subtitle: "Personalized AI Mentorship",
      description: "8 specialized AI agents adapt to your unique learning style, pace, and goals. Get instant feedback, interactive lessons, and 24/7 support.",
      features: [
        "Adaptive learning paths",
        "Real-time feedback",
        "Interactive simulations",
        "24/7 AI availability"
      ],
      gradient: "gradient-stella"
    },
    {
      icon: ShieldCheck,
      title: "Verify",
      subtitle: "Blockchain Credentials",
      description: "Every achievement is recorded on the blockchain as an immutable, verifiable credential. Your education becomes a permanent digital passport.",
      features: [
        "Immutable records",
        "Global recognition",
        "Instant verification",
        "Tamper-proof credentials"
      ],
      gradient: "gradient-max"
    },
    {
      icon: Gem,
      title: "Own",
      subtitle: "Education as Capital",
      description: "You own your learning data forever. Earn tokens for achievements, trade them, or use them to unlock premium content. Your education, your asset.",
      features: [
        "Earn learning tokens",
        "Tradeable achievements",
        "Lifetime ownership",
        "Portable portfolio"
      ],
      gradient: "gradient-darwin"
    }
  ];

  return (
    <section className="py-24 bg-gradient-to-b from-secondary/20 to-background">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="text-center mb-20 space-y-4"
        >
          <h2 className="text-4xl sm:text-5xl lg:text-6xl font-black">
            <span className="gradient-text">Learn. Verify. Own.</span>
          </h2>
          <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
            The three pillars of the Stellecta revolution
          </p>
        </motion.div>

        {/* Pillars Grid */}
        <div className="grid md:grid-cols-3 gap-8">
          {pillars.map((pillar, index) => (
            <motion.div
              key={pillar.title}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6, delay: index * 0.2 }}
              className="group relative"
            >
              <div className="h-full bg-card rounded-3xl p-8 shadow-lg hover:shadow-2xl transition-all duration-300 border border-border hover:border-primary/30">
                {/* Icon */}
                <div className={`w-16 h-16 rounded-2xl ${pillar.gradient} flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300`}>
                  <pillar.icon className="h-8 w-8 text-white" />
                </div>

                {/* Content */}
                <h3 className="text-3xl font-black mb-2">{pillar.title}</h3>
                <p className="text-sm font-semibold text-primary mb-4">{pillar.subtitle}</p>
                <p className="text-muted-foreground mb-6 leading-relaxed">
                  {pillar.description}
                </p>

                {/* Features List */}
                <ul className="space-y-3">
                  {pillar.features.map((feature) => (
                    <li key={feature} className="flex items-start gap-2">
                      <div className="w-1.5 h-1.5 rounded-full bg-primary mt-2 flex-shrink-0" />
                      <span className="text-sm text-muted-foreground">{feature}</span>
                    </li>
                  ))}
                </ul>

                {/* Hover Glow */}
                <div className="absolute inset-0 rounded-3xl opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none">
                  <div className={`absolute inset-0 ${pillar.gradient} opacity-5 rounded-3xl`} />
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default ThreePillars;
