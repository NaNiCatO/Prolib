"use client"
import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import { SidebarInset, SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar";
import { AppSidebar } from "@/components/app-sidebar";
import "./globals.css";
import { usePathname } from "next/navigation";
import ChatWidget from "./ui/chat-widget";

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const pathname = usePathname();

  return (
    <html>
      <body className={pathname === "/" ? "overflow-hidden" : "overflow-auto"}>
        <SidebarProvider>
          <AppSidebar />
          <SidebarInset>
            <main>
              <SidebarTrigger size={"icon"} />
              <ChatWidget />
              {children}
            </main>
          </SidebarInset>
        </SidebarProvider>
      </body>
    </html>

  );
}
