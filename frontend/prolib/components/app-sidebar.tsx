import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/components/ui/sidebar"
import { BookText, BookPlus, BookCopy, Globe, Library, Package, Info, Settings, LogOut } from "lucide-react"
import Link from "next/link"

export function AppSidebar() {
  return (
    <Sidebar collapsible="icon" variant="sidebar">
      <SidebarHeader>
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton asChild size={"title"}>
              <Link href={"/"}>
                <BookText className="sidebar-icons" />
                <span className="text-2xl">ProLib</span>
              </Link>
            </SidebarMenuButton >
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarHeader>
      <SidebarContent>
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton asChild size={"huge"}>
              <Link href={"library"}>
                <Globe className="sidebar-icons" />
                <span>Library</span>
              </Link>
            </SidebarMenuButton>
          </SidebarMenuItem>
          <SidebarMenuItem>
            <SidebarMenuButton asChild size={"huge"}>
              <Link href={"addBook"}>
                <BookPlus className="sidebar-icons" />
                <span>Add Book</span>
              </Link>
            </SidebarMenuButton>
          </SidebarMenuItem>
          <SidebarMenuItem>
            <SidebarMenuButton asChild size={"huge"}>
              <Link href={"myCatalog"}>
                <Library className="sidebar-icons" />
                <span>My Catalog</span>
              </Link>
            </SidebarMenuButton>
          </SidebarMenuItem>
          <SidebarMenuItem>
            <SidebarMenuButton asChild size={"huge"}>
              <Link href={"myCollections"}>
                <Package className="sidebar-icons" />
                <span>My Collections</span>
              </Link>
            </SidebarMenuButton>
          </SidebarMenuItem>
          <SidebarMenuItem>
            <SidebarMenuButton asChild size={"huge"}>
              <Link href={"Settings"}>
                <Settings className="sidebar-icons" />
                <span>Settings</span>
              </Link>
            </SidebarMenuButton>
          </SidebarMenuItem>
          <SidebarMenuItem>
            <SidebarMenuButton asChild size={"huge"}>
              <Link href={"Support"}>
                <Info className="sidebar-icons" />
                <span>Support</span>
              </Link>
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarContent>
      <SidebarFooter>
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton asChild size={"lg"}>
              <Link href={"logOut"}>
                Logout
                <LogOut className="sidebar-icons" />
              </Link>
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarFooter>
    </Sidebar>
  )
}
