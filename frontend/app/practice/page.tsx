"use client";

import YogaCamera from "@/components/yoga/YogaCamera";
import Link from "next/link";
import { ArrowLeft } from "lucide-react";
import { motion } from "framer-motion";

export default function PracticePage() {
    return (
        <div className="fixed inset-0 bg-[#FAF3EF] overflow-hidden flex flex-col">
            {/* Minimal Header */}
            <motion.div
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
                className="absolute top-0 left-0 right-0 p-6 z-50 flex items-center justify-between"
            >
                <Link href="/" className="flex items-center gap-2 text-[#3E5E6B]/70 hover:text-[#3E5E6B] transition-colors group">
                    <div className="w-10 h-10 rounded-full bg-[#3E5E6B]/10 flex items-center justify-center group-hover:bg-[#3E5E6B]/20 transition-all">
                        <ArrowLeft className="w-5 h-5" />
                    </div>
                </Link>
                <span className="text-[#3E5E6B]/50 text-xs font-bold uppercase tracking-widest">Zenva • Practice Mode</span>
            </motion.div>


            {/* Main Content */}
            <motion.div
                initial={{ opacity: 0, scale: 0.98 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.8 }}
                className="flex-1 w-full h-full"
            >
                <YogaCamera />
            </motion.div>
        </div>
    );
}
