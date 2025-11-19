import { motion } from "framer-motion";
import { Shield, Globe, Coins, Lock } from "lucide-react";

const BlockchainSection = () => {
  const features = [
    {
      icon: Shield,
      title: "Immutable Credentials",
      description: "Your achievements are permanently recorded on the blockchain, impossible to forge or lose."
    },
    {
      icon: Globe,
      title: "Global Recognition",
      description: "Accepted worldwide by universities and employers. Your credentials travel with you anywhere."
    },
    {
      icon: Coins,
      title: "Earn Learning Tokens",
      description: "Convert achievements into tradeable tokens. Your education becomes a valuable digital asset."
    },
    {
      icon: Lock,
      title: "You Own Your Data",
      description: "Complete control over your education records. Share only what you want, when you want."
    }
  ];

  return (
    <section className="py-24 bg-gradient-to-b from-background to-secondary/20 relative overflow-hidden">
      {/* Background Elements */}
      <div className="absolute inset-0 overflow-hidden opacity-10">
        <div className="absolute top-20 left-20 w-64 h-64 bg-primary rounded-full blur-3xl" />
        <div className="absolute bottom-20 right-20 w-96 h-96 bg-accent rounded-full blur-3xl" />
      </div>

      <div className="container mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          {/* Left Column - Text */}
          <motion.div
            initial={{ opacity: 0, x: -30 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
            className="space-y-8"
          >
            <div>
              <h2 className="text-4xl sm:text-5xl lg:text-6xl font-black mb-4">
                Your Learning Journey,{" "}
                <span className="gradient-text">Verified Forever</span>
              </h2>
              <p className="text-xl text-muted-foreground leading-relaxed">
                Stellecta creates your Longitudinal Competency Trajectory (LCT) — 
                a lifelong digital education passport secured on the blockchain.
              </p>
            </div>

            {/* Features Grid */}
            <div className="grid sm:grid-cols-2 gap-6">
              {features.map((feature, index) => (
                <motion.div
                  key={feature.title}
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ duration: 0.5, delay: index * 0.1 }}
                  className="space-y-2"
                >
                  <div className="w-12 h-12 rounded-xl bg-primary/10 flex items-center justify-center mb-3">
                    <feature.icon className="h-6 w-6 text-primary" />
                  </div>
                  <h3 className="font-bold text-lg">{feature.title}</h3>
                  <p className="text-sm text-muted-foreground leading-relaxed">
                    {feature.description}
                  </p>
                </motion.div>
              ))}
            </div>
          </motion.div>

          {/* Right Column - Visual */}
          <motion.div
            initial={{ opacity: 0, x: 30 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
            className="relative"
          >
            <div className="relative">
              {/* Main Card */}
              <div className="bg-card rounded-3xl p-8 shadow-2xl border border-border">
                <div className="space-y-6">
                  <div className="flex items-center justify-between">
                    <h3 className="text-2xl font-black">Digital Credential</h3>
                    <div className="px-4 py-1.5 rounded-full bg-primary/10 border border-primary/20">
                      <span className="text-xs font-bold text-primary">VERIFIED</span>
                    </div>
                  </div>

                  {/* Mock Credential */}
                  <div className="space-y-4">
                    <div className="flex items-center gap-4">
                      <div className="w-16 h-16 rounded-2xl gradient-stella flex items-center justify-center text-3xl">
                        📐
                      </div>
                      <div>
                        <p className="font-bold">Advanced Calculus</p>
                        <p className="text-sm text-muted-foreground">Issued by Stella • Mathematics</p>
                      </div>
                    </div>

                    <div className="grid grid-cols-2 gap-4 pt-4 border-t border-border">
                      <div>
                        <p className="text-xs text-muted-foreground">Score</p>
                        <p className="text-2xl font-black gradient-text">95%</p>
                      </div>
                      <div>
                        <p className="text-xs text-muted-foreground">XP Earned</p>
                        <p className="text-2xl font-black gradient-text">1,250</p>
                      </div>
                    </div>

                    <div className="pt-4 border-t border-border space-y-2">
                      <div className="flex justify-between text-xs">
                        <span className="text-muted-foreground">Blockchain ID:</span>
                        <span className="font-mono font-semibold">0x7a8f...2b4c</span>
                      </div>
                      <div className="flex justify-between text-xs">
                        <span className="text-muted-foreground">Network:</span>
                        <span className="font-semibold">Polygon</span>
                      </div>
                      <div className="flex justify-between text-xs">
                        <span className="text-muted-foreground">Date Issued:</span>
                        <span className="font-semibold">Nov 5, 2025</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Floating Elements */}
              <motion.div
                animate={{ y: [0, -10, 0] }}
                transition={{ duration: 3, repeat: Infinity }}
                className="absolute -top-4 -right-4 bg-card p-4 rounded-2xl shadow-xl border-2 border-primary/20"
              >
                <Shield className="h-8 w-8 text-primary" />
              </motion.div>

              <motion.div
                animate={{ y: [0, 10, 0] }}
                transition={{ duration: 3.5, repeat: Infinity }}
                className="absolute -bottom-4 -left-4 bg-card p-4 rounded-2xl shadow-xl border-2 border-accent/20"
              >
                <Coins className="h-8 w-8 text-accent" />
              </motion.div>
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  );
};

export default BlockchainSection;
