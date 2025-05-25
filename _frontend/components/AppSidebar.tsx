'use client'

import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarGroupLabel,
  SidebarHeader,
  SidebarGroupContent,
  SidebarMenu,
  SidebarMenuItem,
  SidebarMenuButton
} from "@/components/ui/sidebar"
import { Rocket, LayoutDashboard, BrainCircuit } from "lucide-react"

export function AppSidebar() {
  return (
    <Sidebar>
      <SidebarHeader />
      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupLabel className="flex items-center gap-2">
            <Rocket className="w-4 h-4" />
            Research Rocket
          </SidebarGroupLabel>

          <SidebarGroupContent>
            <SidebarMenu>
              <SidebarMenuItem key="main-space">
                <SidebarMenuButton asChild>
                  <a href="/workspace" className="flex items-center gap-2">
                    <LayoutDashboard className="w-4 h-4" />
                    <span>Workspace</span>
                  </a>
                </SidebarMenuButton>

                <SidebarMenuButton asChild>
                  <a href="/bro-brain" className="flex items-center gap-2">
                    <BrainCircuit className="w-4 h-4" />
                    <span>Bro Brain</span>
                  </a>
                </SidebarMenuButton>
              </SidebarMenuItem>
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>
      <SidebarFooter />
    </Sidebar>
  )
}

