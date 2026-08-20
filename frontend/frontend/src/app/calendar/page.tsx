"use client";

import { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import {
  ArrowLeft,
  CalendarDays,
  ChevronLeft,
  ChevronRight,
  Clock,
  Plus,
  Trash2,
} from "lucide-react";

import { api } from "@/lib/api";
import { useAuthStore } from "@/lib/auth";

interface Post {
  id: string;
  caption: string;
  image_url: string;
  status: string;
  platforms: string[];
  scheduled_at: string | null;
  published_at: string | null;
  created_at: string;
}

interface PostsResponse {
  posts: Post[];
  total: number;
}

export default function CalendarPage() {
  const token = useAuthStore((state) => state.token);

  const [posts, setPosts] = useState<Post[]>([]);
  const [loading, setLoading] = useState(true);
  const [deletingId, setDeletingId] = useState<string | null>(null);

  const [currentDate, setCurrentDate] = useState(new Date());

  async function loadPosts() {
    if (!token) return;

    try {
      setLoading(true);

      const response = await api.get<PostsResponse>("/posts", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      setPosts(response.data.posts || []);
    } catch (error) {
      console.error("Failed to load posts:", error);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadPosts();
  }, [token]);

  const year = currentDate.getFullYear();
  const month = currentDate.getMonth();

  const monthName = currentDate.toLocaleDateString("en-IN", {
    month: "long",
    year: "numeric",
  });

  const daysInMonth = new Date(year, month + 1, 0).getDate();

  const firstDay = new Date(year, month, 1).getDay();

  const calendarDays = useMemo(() => {
    const days: (number | null)[] = [];

    // Convert Sunday=0 to Monday-first calendar
    const mondayOffset = firstDay === 0 ? 6 : firstDay - 1;

    for (let i = 0; i < mondayOffset; i++) {
      days.push(null);
    }

    for (let day = 1; day <= daysInMonth; day++) {
      days.push(day);
    }

    return days;
  }, [year, month, daysInMonth, firstDay]);

  function previousMonth() {
    setCurrentDate(new Date(year, month - 1, 1));
  }

  function nextMonth() {
    setCurrentDate(new Date(year, month + 1, 1));
  }

  function goToday() {
    setCurrentDate(new Date());
  }

  function postsForDay(day: number) {
    return posts.filter((post) => {
      if (!post.scheduled_at) return false;

      const date = new Date(post.scheduled_at);

      return (
        date.getFullYear() === year &&
        date.getMonth() === month &&
        date.getDate() === day
      );
    });
  }

  function formatTime(value: string) {
    return new Date(value).toLocaleTimeString("en-IN", {
      hour: "numeric",
      minute: "2-digit",
      hour12: true,
    });
  }

  async function cancelScheduledPost(postId: string) {
    const confirmed = window.confirm(
      "Cancel this scheduled post? This will remove it from your calendar."
    );

    if (!confirmed) return;

    if (!token) {
      alert("You are not authenticated.");
      return;
    }

    try {
      setDeletingId(postId);

      await api.delete(`/posts/${postId}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      setPosts((current) =>
        current.filter((post) => post.id !== postId)
      );
    } catch (error: any) {
      console.error("Failed to cancel scheduled post:", error);
      alert(
        error.response?.data?.detail ||
          "Failed to cancel scheduled post."
      );
    } finally {
      setDeletingId(null);
    }
  }

  return (
    <div className="min-h-screen bg-zinc-950 text-white">
      <header className="border-b border-zinc-800">
        <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-6">
          <div className="flex items-center gap-4">
            <Link
              href="/dashboard"
              className="rounded-lg p-2 text-zinc-400 hover:bg-zinc-800 hover:text-white"
            >
              <ArrowLeft size={20} />
            </Link>

            <div className="flex items-center gap-3">
              <CalendarDays size={20} />

              <div>
                <h1 className="font-semibold">Content Calendar</h1>

                <p className="text-xs text-zinc-500">
                  Manage your scheduled content
                </p>
              </div>
            </div>
          </div>

          <Link
            href="/create-post"
            className="inline-flex items-center gap-2 rounded-lg bg-white px-4 py-2 text-sm font-medium text-black hover:bg-zinc-200"
          >
            <Plus size={16} />
            Create Post
          </Link>
        </div>
      </header>

      <main className="mx-auto max-w-7xl p-6 lg:p-8">
        {/* Calendar header */}
        <section className="rounded-2xl border border-zinc-800 bg-zinc-900">
          <div className="flex flex-col gap-4 border-b border-zinc-800 p-5 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <h2 className="text-xl font-semibold">{monthName}</h2>

              <p className="mt-1 text-sm text-zinc-500">
                {loading
                  ? "Loading posts..."
                  : `${posts.length} total posts`}
              </p>
            </div>

            <div className="flex items-center gap-2">
              <button
                onClick={goToday}
                className="rounded-lg border border-zinc-700 px-3 py-2 text-sm text-zinc-300 hover:bg-zinc-800"
              >
                Today
              </button>

              <button
                onClick={previousMonth}
                className="rounded-lg border border-zinc-800 p-2 hover:bg-zinc-800"
              >
                <ChevronLeft size={18} />
              </button>

              <button
                onClick={nextMonth}
                className="rounded-lg border border-zinc-800 p-2 hover:bg-zinc-800"
              >
                <ChevronRight size={18} />
              </button>
            </div>
          </div>

          {/* Weekdays */}
          <div className="grid grid-cols-7 border-b border-zinc-800">
            {[
              "Monday",
              "Tuesday",
              "Wednesday",
              "Thursday",
              "Friday",
              "Saturday",
              "Sunday",
            ].map((day) => (
              <div
                key={day}
                className="border-r border-zinc-800 p-3 text-center text-xs font-medium text-zinc-500 last:border-r-0"
              >
                <span className="hidden sm:inline">{day}</span>
                <span className="sm:hidden">{day.slice(0, 3)}</span>
              </div>
            ))}
          </div>

          {/* Calendar */}
          <div className="grid grid-cols-7">
            {calendarDays.map((day, index) => {
              const dayPosts = day ? postsForDay(day) : [];

              const isToday =
                day !== null &&
                new Date().getFullYear() === year &&
                new Date().getMonth() === month &&
                new Date().getDate() === day;

              return (
                <div
                  key={`${day}-${index}`}
                  className="min-h-32 border-r border-b border-zinc-800 p-2 last:border-r-0 sm:min-h-40"
                >
                  {day && (
                    <>
                      <div className="flex justify-end">
                        <span
                          className={`flex h-7 w-7 items-center justify-center rounded-full text-xs ${
                            isToday
                              ? "bg-white font-bold text-black"
                              : "text-zinc-500"
                          }`}
                        >
                          {day}
                        </span>
                      </div>

                      <div className="mt-2 space-y-2">
                        {dayPosts.map((post) => (
                          <div
                            key={post.id}
                            className="rounded-lg border border-yellow-900/60 bg-yellow-950/30 p-2"
                          >
                            <div className="flex items-center gap-1 text-[10px] text-yellow-400">
                              <Clock size={11} />

                              {formatTime(post.scheduled_at!)}
                            </div>

                            <p className="mt-1 line-clamp-2 text-xs font-medium text-zinc-200">
                              {post.caption}
                            </p>

                            <p className="mt-1 text-[10px] text-zinc-500">
                              {post.platforms?.join(" · ")}
                            </p>

                            <div className="mt-2 flex items-center justify-between gap-2">
                              <span className="text-[10px] text-yellow-500">
                                Scheduled
                              </span>

                              <button
                                onClick={() =>
                                  cancelScheduledPost(post.id)
                                }
                                disabled={deletingId === post.id}
                                className="rounded-md border border-red-900/60 p-1.5 text-red-400 transition hover:bg-red-950 hover:text-red-300 disabled:cursor-not-allowed disabled:opacity-50"
                                title="Cancel scheduled post"
                              >
                                <Trash2 size={13} />
                              </button>
                            </div>
                          </div>
                        ))}
                      </div>
                    </>
                  )}
                </div>
              );
            })}
          </div>
        </section>

        {/* Scheduled posts */}
        <section className="mt-6">
          <div className="mb-4">
            <h2 className="font-semibold">Scheduled Posts</h2>

            <p className="text-sm text-zinc-500">
              Upcoming content waiting to be published
            </p>
          </div>

          <div className="space-y-3">
            {posts
              .filter((post) => post.status === "scheduled")
              .sort(
                (a, b) =>
                  new Date(a.scheduled_at!).getTime() -
                  new Date(b.scheduled_at!).getTime()
              )
              .map((post) => (
                <div
                  key={post.id}
                  className="flex flex-col gap-4 rounded-xl border border-zinc-800 bg-zinc-900 p-4 sm:flex-row sm:items-center"
                >
                  <img
                    src={post.image_url}
                    alt=""
                    className="h-20 w-20 rounded-lg object-cover"
                  />

                  <div className="flex-1">
                    <p className="font-medium">{post.caption}</p>

                    <p className="mt-1 text-sm text-zinc-500">
                      {new Date(post.scheduled_at!).toLocaleString("en-IN", {
                        dateStyle: "medium",
                        timeStyle: "short",
                      })}
                    </p>

                    <p className="mt-1 text-xs text-zinc-600">
                      {post.platforms?.join(" · ")}
                    </p>
                  </div>

                  <div className="flex items-center gap-2">
                    <span className="rounded-full border border-yellow-800 bg-yellow-950/40 px-3 py-1 text-xs text-yellow-400">
                      Scheduled
                    </span>

                    <button
                      onClick={() => cancelScheduledPost(post.id)}
                      disabled={deletingId === post.id}
                      className="inline-flex items-center justify-center gap-2 rounded-lg border border-red-900/60 px-3 py-2 text-xs text-red-400 transition hover:bg-red-950 hover:text-red-300 disabled:cursor-not-allowed disabled:opacity-50"
                    >
                      <Trash2 size={14} />
                      {deletingId === post.id
                        ? "Cancelling..."
                        : "Cancel"}
                    </button>
                  </div>
                </div>
              ))}

            {!loading &&
              posts.filter((post) => post.status === "scheduled")
                .length === 0 && (
                <div className="rounded-xl border border-zinc-800 bg-zinc-900 p-10 text-center">
                  <CalendarDays
                    size={32}
                    className="mx-auto text-zinc-600"
                  />

                  <p className="mt-3 text-sm text-zinc-400">
                    No scheduled posts
                  </p>

                  <p className="mt-1 text-xs text-zinc-600">
                    Schedule a post and it will appear here.
                  </p>
                </div>
              )}
          </div>
        </section>
      </main>
    </div>
  );
}