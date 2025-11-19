import { Github, Twitter, Linkedin, Mail } from "lucide-react";
import stellarLogo from "@/assets/stellar-logo-new.svg";

const Footer = () => {
  const footerSections = [
    {
      title: "Platform",
      links: [
        { name: "For Students", href: "#students" },
        { name: "For Teachers", href: "#teachers" },
        { name: "For Parents", href: "#parents" },
        { name: "For Schools", href: "#schools" }
      ]
    },
    {
      title: "Resources",
      links: [
        { name: "Documentation", href: "#" },
        { name: "API Reference", href: "#" },
        { name: "Tutorials", href: "#" },
        { name: "Blog", href: "#" }
      ]
    },
    {
      title: "Company",
      links: [
        { name: "About Us", href: "#" },
        { name: "Careers", href: "#" },
        { name: "Press Kit", href: "#" },
        { name: "Contact", href: "#" }
      ]
    },
    {
      title: "Legal",
      links: [
        { name: "Privacy Policy", href: "#" },
        { name: "Terms of Service", href: "#" },
        { name: "GDPR", href: "#" },
        { name: "COPPA Compliance", href: "#" }
      ]
    }
  ];

  return (
    <footer className="bg-[hsl(222,47%,11%)] text-white py-16">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid md:grid-cols-2 lg:grid-cols-6 gap-12 mb-12">
          {/* Brand Column */}
          <div className="lg:col-span-2 space-y-4">
            <div className="flex items-center gap-3">
              <img src={stellarLogo} alt="Stellecta" className="h-10 w-auto" />
              <span className="text-2xl font-black gradient-text">Stellecta</span>
            </div>
            <p className="text-sm text-gray-400 leading-relaxed">
              Transform learning into lifelong, verifiable assets with AI-powered education 
              and blockchain credentials.
            </p>
            <div className="flex gap-3">
              <a href="#" className="p-2 rounded-lg bg-white/10 hover:bg-white/20 transition-colors">
                <Twitter className="h-5 w-5" />
              </a>
              <a href="#" className="p-2 rounded-lg bg-white/10 hover:bg-white/20 transition-colors">
                <Linkedin className="h-5 w-5" />
              </a>
              <a href="#" className="p-2 rounded-lg bg-white/10 hover:bg-white/20 transition-colors">
                <Github className="h-5 w-5" />
              </a>
              <a href="#" className="p-2 rounded-lg bg-white/10 hover:bg-white/20 transition-colors">
                <Mail className="h-5 w-5" />
              </a>
            </div>
          </div>

          {/* Links Columns */}
          {footerSections.map((section) => (
            <div key={section.title} className="space-y-4">
              <h3 className="font-bold text-sm uppercase tracking-wider">{section.title}</h3>
              <ul className="space-y-2">
                {section.links.map((link) => (
                  <li key={link.name}>
                    <a
                      href={link.href}
                      onClick={(e) => {
                        if (link.href.startsWith('#')) {
                          e.preventDefault();
                          const sectionName = link.href.substring(1);
                          const event = new CustomEvent('navigate-section', { detail: sectionName });
                          window.dispatchEvent(event);
                        }
                      }}
                      className="text-sm text-gray-400 hover:text-white transition-colors"
                    >
                      {link.name}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        {/* Bottom Bar */}
        <div className="pt-8 border-t border-white/10">
          <div className="flex flex-col md:flex-row justify-between items-center gap-4">
            <p className="text-sm text-gray-400">
              © 2025 Stellecta. All rights reserved.
            </p>
            <div className="flex flex-wrap gap-6 text-sm text-gray-400">
              <a href="#" className="hover:text-white transition-colors">English</a>
              <a href="#" className="hover:text-white transition-colors">Deutsch</a>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
