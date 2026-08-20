"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

import {
  BarChart3,
  CalendarDays,
  FileText,
  Home,
  LogOut,
  Plus,
  Settings,
  Share2,
  Camera,
  Sparkles,
} from "lucide-react";

import { useAuthStore } from "@/lib/auth";
import { api } from "@/lib/api";
interface Post {
  id: string;
  caption: string;
  image_url: string;
  status: string;
  facebook_post_id: string | null;
  instagram_media_id: string | null;
  published_at: string | null;
  created_at: string;
}

interface PostsResponse {
  posts: Post[];
  total: number;
}
export default function DashboardPage() {
  const router = useRouter();

  const user = useAuthStore((state) => state.user);
  const clearAuth = useAuthStore((state) => state.clearAuth);
  const token = useAuthStore((state) => state.token);

  const [posts, setPosts] = useState<Post[]>([]);
  const [totalPosts, setTotalPosts] = useState(0);
  const [loadingPosts, setLoadingPosts] = useState(true);

  function handleLogout() {
    clearAuth();
    router.push("/login");
  }

  useEffect(() => {
    async function loadPosts() {
      if (!token) {
        setLoadingPosts(false);
        return;
      }

      try {
        const response = await api.get<PostsResponse>("/posts", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        setPosts(response.data.posts);
        setTotalPosts(response.data.total);
      } catch (error) {
        console.error("Failed to load dashboard posts:", error);
      } finally {
        setLoadingPosts(false);
      }
    }

    loadPosts();
  }, [token]);

  return (
    <div className="min-h-screen bg-zinc-950 text-white">
      <div className="flex min-h-screen">

        {/* Sidebar */}
        <aside className="hidden w-64 border-r border-zinc-800 bg-zinc-900/70 md:flex md:flex-col">
          <div className="flex h-16 items-center gap-3 border-b border-zinc-800 px-6">
            <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-white font-bold text-black">
              S
            </div>

            <span className="font-semibold">
              SocialAI
            </span>
          </div>

          <nav className="flex-1 space-y-1 p-4">

            <Link
              href="/dashboard"
              className="flex items-center gap-3 rounded-lg bg-zinc-800 px-3 py-2.5 text-sm font-medium"
            >
              <Home size={18} />
              Dashboard
            </Link>

            <Link
              href="/create-post"
              className="flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm text-zinc-400 transition hover:bg-zinc-800 hover:text-white"
            >
              <Plus size={18} />
              Create Post
            </Link>

            <Link
              href="/accounts"
              className="flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm text-zinc-400 transition hover:bg-zinc-800 hover:text-white"
            >
              <Camera size={18} />
              Connected Accounts
            </Link>

            <Link
              href="/posts"
              className="flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm text-zinc-400 transition hover:bg-zinc-800 hover:text-white"
            >
              <FileText size={18} />
              Posts
            </Link>

            <Link
              href="/calendar"
              className="flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm text-zinc-400 transition hover:bg-zinc-800 hover:text-white"
            >
              <CalendarDays size={18} />
              Calendar
            </Link>

            <Link
              href="/analytics"
              className="flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm text-zinc-400 transition hover:bg-zinc-800 hover:text-white"
            >
              <BarChart3 size={18} />
              Analytics
            </Link>

          </nav>

          <div className="border-t border-zinc-800 p-4">

            <Link
              href="/settings"
              className="mb-1 flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm text-zinc-400 transition hover:bg-zinc-800 hover:text-white"
            >
              <Settings size={18} />
              Settings
            </Link>

            <button
              onClick={handleLogout}
              className="flex w-full items-center gap-3 rounded-lg px-3 py-2.5 text-sm text-zinc-400 transition hover:bg-red-950 hover:text-red-300"
            >
              <LogOut size={18} />
              Logout
            </button>

          </div>
        </aside>

        {/* Main */}
        <main className="flex-1">

          {/* Header */}
          <header className="flex h-16 items-center justify-between border-b border-zinc-800 px-6">
            <div>
              <h1 className="text-lg font-semibold">
                Dashboard
              </h1>

              <p className="text-xs text-zinc-500">
                Manage your social media presence
              </p>
            </div>

            <div className="text-right">
              <p className="text-sm font-medium">
                {user?.name || "User"}
              </p>

              <p className="text-xs text-zinc-500">
                {user?.email || ""}
              </p>
            </div>
          </header>

          {/* Content */}
          <div className="space-y-8 p-6 lg:p-8">

            {/* Welcome */}
            <section>
              <h2 className="text-2xl font-semibold">
                Welcome back{user?.name ? `, ${user.name}` : ""} 👋
              </h2>

              <p className="mt-1 text-sm text-zinc-400">
                Create, publish and manage your social content from one place.
              </p>
            </section>

            {/* Create Post CTA */}
            <section className="rounded-2xl border border-zinc-800 bg-gradient-to-br from-zinc-900 to-zinc-950 p-6">
              <div className="flex flex-col justify-between gap-6 md:flex-row md:items-center">

                <div>
                  <div className="mb-3 flex h-10 w-10 items-center justify-center rounded-xl bg-white text-black">
                    <Sparkles size={20} />
                  </div>

                  <h3 className="text-xl font-semibold">
                    Create your next post
                  </h3>

                  <p className="mt-1 max-w-xl text-sm text-zinc-400">
                    Write a caption manually or use AI to generate a draft,
                    upload your media and publish to your connected platforms.
                  </p>
                </div>

                <Link
                  href="/create-post"
                  className="inline-flex items-center justify-center gap-2 rounded-lg bg-white px-5 py-3 text-sm font-medium text-black transition hover:bg-zinc-200"
                >
                  <Plus size={18} />
                  Create Post
                </Link>

              </div>
            </section>

            {/* Stats */}
            <section className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">

              <div className="rounded-xl border border-zinc-800 bg-zinc-900 p-5">
                <p className="text-sm text-zinc-500">
                  Facebook
                </p>

                <div className="mt-3 flex items-center gap-3">
                  <Share2 size={20} />
                  <span className="text-lg font-semibold">
                    Connected
                  </span>
                </div>
              </div>

              <div className="rounded-xl border border-zinc-800 bg-zinc-900 p-5">
                <p className="text-sm text-zinc-500">
                  Instagram
                </p>

                <div className="mt-3 flex items-center gap-3">
                  <Camera size={20} />
                  <span className="text-lg font-semibold">
                    Connected
                  </span>
                </div>
              </div>

              <div className="rounded-xl border border-zinc-800 bg-zinc-900 p-5">
                <p className="text-sm text-zinc-500">
                  Posts
                </p>

                <p className="mt-3 text-2xl font-semibold">
                  {loadingPosts ? "..." : totalPosts}
                </p>
              </div>

              <div className="rounded-xl border border-zinc-800 bg-zinc-900 p-5">
                <p className="text-sm text-zinc-500">
                  Scheduled
                </p>

                <p className="mt-3 text-2xl font-semibold">
                  —
                </p>
              </div>

            </section>

            {/* Recent Activity */}
            <section>

              <div className="mb-4 flex items-center justify-between">
                <div>
                  <h3 className="font-semibold">
                    Recent Activity
                  </h3>

                  <p className="text-sm text-zinc-500">
                    Your latest publishing activity
                  </p>
                </div>

                <Link
                  href="/posts"
                  className="text-sm text-zinc-400 hover:text-white"
                >
                  View all
                </Link>
              </div>

              {loadingPosts ? (
                <div className="rounded-xl border border-zinc-800 bg-zinc-900 p-10 text-center">
                  <p className="text-sm text-zinc-500">
                    Loading activity...
                  </p>
                </div>
              ) : posts.length === 0 ? (
                <div className="rounded-xl border border-zinc-800 bg-zinc-900 p-10 text-center">
                  <FileText
                    className="mx-auto text-zinc-600"
                    size={32}
                  />

                  <p className="mt-3 text-sm text-zinc-400">
                    No posts yet
                  </p>

                  <p className="mt-1 text-xs text-zinc-600">
                    Your published posts will appear here.
                  </p>
                </div>
              ) : (
                <div className="space-y-3">
                  {posts.slice(0, 3).map((post) => (
                    <div
                      key={post.id}
                      className="flex items-center gap-4 rounded-xl border border-zinc-800 bg-zinc-900 p-4"
                    >
                      <img
                        src={post.image_url}
                        alt="Post"
                        className="h-16 w-16 rounded-lg object-cover"
                      />

                      <div className="min-w-0 flex-1">
                        <p className="truncate text-sm font-medium">
                          {post.caption}
                        </p>

                        <p className="mt-1 text-xs text-zinc-500">
                          {post.published_at
                            ? new Date(post.published_at).toLocaleString(
                                "en-IN",
                                {
                                  dateStyle: "medium",
                                  timeStyle: "short",
                                }
                              )
                            : "Not published"}
                        </p>
                      </div>

                      <div
                        className={`rounded-full px-3 py-1 text-xs ${
                          post.status === "published"
                            ? "bg-emerald-950 text-emerald-400"
                            : post.status === "partial"
                            ? "bg-yellow-950 text-yellow-400"
                            : "bg-red-950 text-red-400"
                        }`}
                      >
                        {post.status}
                      </div>
                    </div>
                  ))}
                </div>
              )}

            </section>

          </div>
        </main>
      </div>
    </div>
  );
}