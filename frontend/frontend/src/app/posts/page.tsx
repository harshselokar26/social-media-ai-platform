"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import {
  ArrowLeft,
  CheckCircle2,
  Clock,
  FileText,
  Trash2,
  XCircle,
  Loader2,
} from "lucide-react";

import { api } from "@/lib/api";
import { useAuthStore } from "@/lib/auth";

interface Post {
  id: string;
  user_id: string;
  organization_id: string | null;

  caption: string;
  image_url: string;
  status: string;

  platforms: string[];

  facebook_post_id: string | null;
  instagram_media_id: string | null;

  error_message: string | null;

  published_at: string | null;
  scheduled_at: string | null;

  created_at: string;
  updated_at: string;
}

interface PostsResponse {
  posts: Post[];
  total: number;
}

type Filter =
  | "all"
  | "published"
  | "scheduled"
  | "partial"
  | "failed";

function StatusBadge({ status }: { status: string }) {
  if (status === "published") {
    return (
      <span className="inline-flex items-center gap-1.5 rounded-full bg-emerald-950 px-3 py-1 text-xs font-medium text-emerald-400">
        <CheckCircle2 size={14} />
        Published
      </span>
    );
  }

  if (status === "scheduled") {
    return (
      <span className="inline-flex items-center gap-1.5 rounded-full bg-blue-950 px-3 py-1 text-xs font-medium text-blue-400">
        <Clock size={14} />
        Scheduled
      </span>
    );
  }

  if (status === "partial") {
    return (
      <span className="inline-flex items-center gap-1.5 rounded-full bg-yellow-950 px-3 py-1 text-xs font-medium text-yellow-400">
        <Clock size={14} />
        Partial
      </span>
    );
  }

  if (status === "publishing") {
    return (
      <span className="inline-flex items-center gap-1.5 rounded-full bg-purple-950 px-3 py-1 text-xs font-medium text-purple-400">
        <Loader2 size={14} className="animate-spin" />
        Publishing
      </span>
    );
  }

  return (
    <span className="inline-flex items-center gap-1.5 rounded-full bg-red-950 px-3 py-1 text-xs font-medium text-red-400">
      <XCircle size={14} />
      Failed
    </span>
  );
}

function formatDate(date: string | null) {
  if (!date) return "Not available";

  return new Date(date).toLocaleString("en-IN", {
    dateStyle: "medium",
    timeStyle: "short",
  });
}

function getPostDate(post: Post) {
  if (post.status === "scheduled" && post.scheduled_at) {
    return post.scheduled_at;
  }

  if (post.published_at) {
    return post.published_at;
  }

  return post.created_at;
}

function PlatformStatus({
  platform,
  published,
  scheduled,
}: {
  platform: string;
  published: boolean;
  scheduled: boolean;
}) {
  let statusText = "Not published";
  let statusClass = "text-zinc-500";
  let containerClass = "border-zinc-800 bg-zinc-950";

  if (published) {
    statusText = "Published";
    statusClass = "text-emerald-400";
    containerClass = "border-emerald-900 bg-emerald-950/20";
  } else if (scheduled) {
    statusText = "Scheduled";
    statusClass = "text-blue-400";
    containerClass = "border-blue-900 bg-blue-950/20";
  }

  return (
    <div
      className={`flex items-center justify-between rounded-lg border px-3 py-2 ${containerClass}`}
    >
      <div className="flex items-center gap-2">
        <span className="text-lg font-bold">
          {platform === "facebook" ? "f" : "◎"}
        </span>

        <span className="text-sm capitalize">
          {platform}
        </span>
      </div>

      <span className={`text-xs ${statusClass}`}>
        {statusText}
      </span>
    </div>
  );
}

export default function PostsPage() {
  const token = useAuthStore((state) => state.token);

  const [posts, setPosts] = useState<Post[]>([]);
  const [total, setTotal] = useState(0);

  const [loading, setLoading] = useState(true);
  const [deletingId, setDeletingId] = useState<string | null>(null);

  const [error, setError] = useState("");

  const [filter, setFilter] = useState<Filter>("all");

  async function loadPosts() {
    if (!token) {
      setLoading(false);
      return;
    }

    try {
      setLoading(true);
      setError("");

      const response = await api.get<PostsResponse>("/posts", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      setPosts(response.data.posts);
      setTotal(response.data.total);
    } catch (err: any) {
      console.error(err);

      setError(
        err?.response?.data?.detail ||
          "Unable to load your posts."
      );
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadPosts();
  }, [token]);

  async function handleDelete(
    event: React.MouseEvent,
    post: Post
  ) {
    event.preventDefault();
    event.stopPropagation();

    if (!token) {
      setError("You are not authenticated.");
      return;
    }

    const isScheduled = post.status === "scheduled";

    const confirmed = window.confirm(
      isScheduled
        ? "Cancel this scheduled post?"
        : "Delete this post?"
    );

    if (!confirmed) return;

    try {
      setDeletingId(post.id);
      setError("");

      await api.delete(`/posts/${post.id}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      setPosts((current) =>
        current.filter((item) => item.id !== post.id)
      );

      setTotal((current) => Math.max(0, current - 1));
    } catch (err: any) {
      console.error(err);

      setError(
        err?.response?.data?.detail ||
          "Unable to delete the post."
      );
    } finally {
      setDeletingId(null);
    }
  }

  const filteredPosts =
    filter === "all"
      ? posts
      : posts.filter((post) => post.status === filter);

  const filters: [Filter, string][] = [
    ["all", "All"],
    ["published", "Published"],
    ["scheduled", "Scheduled"],
    ["partial", "Partial"],
    ["failed", "Failed"],
  ];

  return (
    <div className="min-h-screen bg-zinc-950 text-white">

      {/* Header */}
      <header className="border-b border-zinc-800">
        <div className="mx-auto flex h-16 max-w-6xl items-center justify-between px-6">

          <div className="flex items-center gap-4">
            <Link
              href="/dashboard"
              className="text-zinc-400 transition hover:text-white"
            >
              <ArrowLeft size={20} />
            </Link>

            <div>
              <h1 className="text-lg font-semibold">
                Posts
              </h1>

              <p className="text-xs text-zinc-500">
                View and manage your social media content
              </p>
            </div>
          </div>

          <Link
            href="/create-post"
            className="rounded-lg bg-white px-4 py-2 text-sm font-medium text-black transition hover:bg-zinc-200"
          >
            Create Post
          </Link>
        </div>
      </header>

      {/* Main */}
      <main className="mx-auto max-w-6xl space-y-6 p-6 lg:p-8">

        {/* Title */}
        <section>
          <div className="flex items-center gap-3">
            <FileText size={28} />

            <h2 className="text-3xl font-semibold">
              Your Posts
            </h2>
          </div>

          <p className="mt-2 text-sm text-zinc-500">
            {total} {total === 1 ? "post" : "posts"} total.
          </p>
        </section>

        {/* Filters */}
        <div className="flex flex-wrap gap-2">
          {filters.map(([value, label]) => (
            <button
              key={value}
              onClick={() => setFilter(value)}
              className={`rounded-lg px-4 py-2 text-sm transition ${
                filter === value
                  ? "bg-white text-black"
                  : "border border-zinc-800 bg-zinc-900 text-zinc-400 hover:text-white"
              }`}
            >
              {label}
            </button>
          ))}
        </div>

        {/* Error */}
        {error && (
          <div className="rounded-xl border border-red-800 bg-red-950/40 p-5 text-sm text-red-300">
            {error}
          </div>
        )}

        {/* Loading */}
        {loading && (
          <div className="rounded-xl border border-zinc-800 bg-zinc-900 p-12 text-center text-sm text-zinc-500">
            Loading posts...
          </div>
        )}

        {/* Empty */}
        {!loading &&
          !error &&
          filteredPosts.length === 0 && (
            <div className="rounded-xl border border-zinc-800 bg-zinc-900 p-12 text-center">
              <FileText
                className="mx-auto text-zinc-600"
                size={36}
              />

              <h3 className="mt-4 font-medium">
                No posts found
              </h3>

              <p className="mt-1 text-sm text-zinc-500">
                {filter === "all"
                  ? "Create your first social media post."
                  : `No ${filter} posts found.`}
              </p>
            </div>
          )}

        {/* Posts */}
        {!loading &&
          !error &&
          filteredPosts.length > 0 && (
            <div className="grid gap-5 md:grid-cols-2">

              {filteredPosts.map((post) => {
                const facebookPublished =
                  Boolean(post.facebook_post_id);

                const instagramPublished =
                  Boolean(post.instagram_media_id);

                const facebookScheduled =
                  post.status === "scheduled" &&
                  post.platforms?.includes("facebook");

                const instagramScheduled =
                  post.status === "scheduled" &&
                  post.platforms?.includes("instagram");

                const isDeleting =
                  deletingId === post.id;

                return (
                  <div
                    key={post.id}
                    className="overflow-hidden rounded-2xl border border-zinc-800 bg-zinc-900 transition hover:border-zinc-600"
                  >

                    {/* Clickable content */}
                    <Link
                      href={`/posts/${post.id}`}
                      className="block"
                    >

                      {/* Image */}
                      <div className="aspect-video overflow-hidden bg-zinc-950">
                        <img
                          src={post.image_url}
                          alt="Post"
                          className="h-full w-full object-cover transition duration-300"
                        />
                      </div>

                      {/* Content */}
                      <div className="space-y-5 p-5">

                        {/* Status/date */}
                        <div className="flex items-center justify-between gap-3">
                          <StatusBadge
                            status={post.status}
                          />

                          <span className="text-right text-xs text-zinc-500">
                            {formatDate(
                              getPostDate(post)
                            )}
                          </span>
                        </div>

                        {/* Caption */}
                        <p className="whitespace-pre-wrap text-sm leading-6 text-zinc-300">
                          {post.caption}
                        </p>

                        {/* Platforms */}
                        <div className="space-y-2">

                          {post.platforms?.includes(
                            "facebook"
                          ) && (
                            <PlatformStatus
                              platform="facebook"
                              published={
                                facebookPublished
                              }
                              scheduled={
                                facebookScheduled
                              }
                            />
                          )}

                          {post.platforms?.includes(
                            "instagram"
                          ) && (
                            <PlatformStatus
                              platform="instagram"
                              published={
                                instagramPublished
                              }
                              scheduled={
                                instagramScheduled
                              }
                            />
                          )}

                        </div>

                        {/* Error */}
                        {post.error_message && (
                          <div className="rounded-lg border border-red-900 bg-red-950/30 p-3">
                            <p className="text-xs font-medium text-red-400">
                              Publishing issue
                            </p>

                            <p className="mt-1 text-xs leading-5 text-red-300/80">
                              {post.error_message}
                            </p>
                          </div>
                        )}

                      </div>
                    </Link>

                    {/* Actions */}
                    <div className="border-t border-zinc-800 p-4">

                      <div className="flex items-center justify-between gap-3">

                        <Link
                          href={`/posts/${post.id}`}
                          className="rounded-lg border border-zinc-700 px-4 py-2 text-sm text-zinc-300 transition hover:bg-zinc-800 hover:text-white"
                        >
                          View Details
                        </Link>

                        <button
                          onClick={(event) =>
                            handleDelete(event, post)
                          }
                          disabled={isDeleting}
                          className="flex items-center gap-2 rounded-lg border border-red-900 px-4 py-2 text-sm text-red-400 transition hover:bg-red-950/40 disabled:cursor-not-allowed disabled:opacity-50"
                        >
                          {isDeleting ? (
                            <>
                              <Loader2
                                size={16}
                                className="animate-spin"
                              />

                              {post.status ===
                              "scheduled"
                                ? "Cancelling..."
                                : "Deleting..."}
                            </>
                          ) : (
                            <>
                              <Trash2 size={16} />

                              {post.status ===
                              "scheduled"
                                ? "Cancel"
                                : "Delete"}
                            </>
                          )}
                        </button>

                      </div>

                    </div>
                  </div>
                );
              })}

            </div>
          )}

      </main>
    </div>
  );
}