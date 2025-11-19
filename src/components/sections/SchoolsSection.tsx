import { motion } from "framer-motion";
import { GraduationCap, Users, BarChart, Shield, Zap, CheckCircle } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useState } from "react";
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { useToast } from "@/hooks/use-toast";
const SchoolsSection = () => {
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [formData, setFormData] = useState({
    schoolName: "",
    contactName: "",
    email: "",
    phone: "",
    studentCount: "",
    message: ""
  });
  const {
    toast
  } = useToast();
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // TODO: Connect to backend when email functionality is added
    console.log("Form submitted:", formData);
    toast({
      title: "Thank you for your interest!",
      description: "We'll get back to you within 24 hours."
    });
    setIsDialogOpen(false);
    setFormData({
      schoolName: "",
      contactName: "",
      email: "",
      phone: "",
      studentCount: "",
      message: ""
    });
  };
  const usps = [{
    icon: GraduationCap,
    title: "Personalized Learning at Scale",
    description: "8 specialized AI agents provide individual support to every student, adapting to their unique learning needs and pace."
  }, {
    icon: BarChart,
    title: "Real-Time Analytics",
    description: "Track student progress, identify learning gaps, and measure outcomes with comprehensive dashboards for teachers and administrators."
  }, {
    icon: Users,
    title: "Easy Integration",
    description: "Seamlessly integrate with your existing LMS and curriculum. Set up in days, not months."
  }, {
    icon: Shield,
    title: "Enterprise Security",
    description: "GDPR and COPPA compliant with bank-level encryption. Your student data is always protected."
  }, {
    icon: Zap,
    title: "Reduce Teacher Workload",
    description: "Automate routine tasks and provide instant feedback, freeing teachers to focus on what matters most."
  }, {
    icon: CheckCircle,
    title: "Proven Results",
    description: "Schools using Stellecta report 35% improvement in student engagement and 28% increase in learning outcomes."
  }];
  return <div className="min-h-screen bg-gradient-to-b from-background via-primary/5 to-background py-24">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div initial={{
        opacity: 0,
        y: 20
      }} animate={{
        opacity: 1,
        y: 0
      }} transition={{
        duration: 0.6
      }} className="text-center space-y-6 mb-16">
          <h1 className="text-5xl sm:text-6xl lg:text-7xl font-black">
            Transform Your School with{" "}
            <span className="gradient-text">AI-Powered Education</span>
          </h1>
          <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
            Join forward-thinking schools worldwide that are revolutionizing education 
            with personalized AI learning, blockchain credentials, and data-driven insights.
          </p>
        </motion.div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8 mb-16">
          {usps.map((usp, index) => <motion.div key={usp.title} initial={{
          opacity: 0,
          y: 20
        }} animate={{
          opacity: 1,
          y: 0
        }} transition={{
          duration: 0.5,
          delay: index * 0.1
        }} className="bg-card rounded-3xl p-8 shadow-lg hover:shadow-xl transition-all border border-border hover:border-primary/50">
              <div className="w-14 h-14 rounded-2xl gradient-stellar flex items-center justify-center mb-4">
                <usp.icon className="h-7 w-7 text-white" />
              </div>
              <h3 className="text-2xl font-black mb-3">{usp.title}</h3>
              <p className="text-muted-foreground leading-relaxed">{usp.description}</p>
            </motion.div>)}
        </div>

        {/* Stats Section */}
        <motion.div initial={{
        opacity: 0,
        y: 20
      }} animate={{
        opacity: 1,
        y: 0
      }} transition={{
        duration: 0.6,
        delay: 0.3
      }} className="bg-gradient-to-br from-primary/10 to-secondary/10 rounded-3xl p-12 mb-16 border border-primary/20">
          <div className="grid md:grid-cols-3 gap-8 text-center">
            <div>
              <div className="text-5xl font-black gradient-text mb-2">Child-Safe Content</div>
              <div className="text-lg text-muted-foreground">AI Filters + Controls</div>
            </div>
            <div>
              <div className="text-5xl font-black gradient-text mb-2">Pedagogical Design</div>
              <div className="text-lg text-muted-foreground">Research-Aligned</div>
            </div>
            <div>
              <div className="text-5xl font-black gradient-text mb-2">Global Curriculum</div>
              <div className="text-lg text-muted-foreground">Aligned to standards</div>
            </div>
          </div>
        </motion.div>

        {/* CTA Section */}
        <motion.div initial={{
        opacity: 0,
        y: 20
      }} animate={{
        opacity: 1,
        y: 0
      }} transition={{
        duration: 0.6,
        delay: 0.6
      }} className="text-center bg-card rounded-3xl p-12 shadow-xl border border-border">
          <h2 className="text-4xl font-black mb-4">Ready to Transform Your School?</h2>
          <p className="text-xl text-muted-foreground mb-8 max-w-2xl mx-auto">
            Schedule a demo and see how Stellecta can help your students succeed. 
            Our team will work with you to create a customized implementation plan.
          </p>
          <Button size="lg" className="gradient-stellar text-white font-bold text-lg px-10 py-7" onClick={() => setIsDialogOpen(true)}>
            Request a Demo
          </Button>
        </motion.div>
      </div>

      {/* Contact Form Dialog */}
      <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
        <DialogContent className="sm:max-w-[500px]">
          <DialogHeader>
            <DialogTitle className="text-2xl font-black">Request a Demo</DialogTitle>
            <DialogDescription>
              Fill out the form below and our team will reach out to schedule a personalized demo.
            </DialogDescription>
          </DialogHeader>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="schoolName">School Name *</Label>
              <Input id="schoolName" required value={formData.schoolName} onChange={e => setFormData({
              ...formData,
              schoolName: e.target.value
            })} placeholder="Enter your school name" />
            </div>
            <div className="space-y-2">
              <Label htmlFor="contactName">Contact Name *</Label>
              <Input id="contactName" required value={formData.contactName} onChange={e => setFormData({
              ...formData,
              contactName: e.target.value
            })} placeholder="Your full name" />
            </div>
            <div className="space-y-2">
              <Label htmlFor="email">Email Address *</Label>
              <Input id="email" type="email" required value={formData.email} onChange={e => setFormData({
              ...formData,
              email: e.target.value
            })} placeholder="your.email@school.edu" />
            </div>
            <div className="space-y-2">
              <Label htmlFor="phone">Phone Number</Label>
              <Input id="phone" type="tel" value={formData.phone} onChange={e => setFormData({
              ...formData,
              phone: e.target.value
            })} placeholder="+1 (555) 123-4567" />
            </div>
            <div className="space-y-2">
              <Label htmlFor="studentCount">Number of Students *</Label>
              <Input id="studentCount" required value={formData.studentCount} onChange={e => setFormData({
              ...formData,
              studentCount: e.target.value
            })} placeholder="e.g., 500" />
            </div>
            <div className="space-y-2">
              <Label htmlFor="message">Message</Label>
              <Textarea id="message" value={formData.message} onChange={e => setFormData({
              ...formData,
              message: e.target.value
            })} placeholder="Tell us about your needs..." rows={4} />
            </div>
            <Button type="submit" className="w-full gradient-stellar text-white font-bold">
              Submit Request
            </Button>
          </form>
        </DialogContent>
      </Dialog>
    </div>;
};
export default SchoolsSection;