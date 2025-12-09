"use client";

import React from "react";
import { Navbar } from "@/components/layout/Navbar";
import { Footer } from "@/components/layout/Footer";
import { Hero } from "@/components/landing/Hero";
import { Features } from "@/components/landing/Features";

export default function LandingPage() {
  return (
    <div className="min-h-screen flex flex-col font-sans text-[#3E5E6B] bg-[#FAF3EF]">
      <Navbar />
      <Hero />
      <Features />
      <Footer />
    </div>
  );
}
