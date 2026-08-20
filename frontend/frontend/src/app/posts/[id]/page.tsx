"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";
import {
  ArrowLeft,
  CheckCircle2,
  Clock,
  XCircle,
//   Facebook,
//   Instagram,
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
  facebook_post_id: string | null;
  instagram_media_id: string | null;
  error_message: string | null;
  published_at: string | null;
  created_at: string;
  updated_at: string;
}

function formatDate(date: string | null) {
  if (!date) return "Not published";

  return new Date(date).toLocaleString("en-IN", {
    dateStyle: "medium",
    timeStyle: "short",
  });
}

function StatusBadge({ status }: { status: string }) {
  if (status === "published") {
    return (
      <span className="inline-flex items-center gap-2 rounded-full bg-emerald-950 px-3 py-1.5 text-sm font-medium text-emerald-400">
        <CheckCircle2 size={16} />
        Published
      </span>
    );
  }

  if (status === "partial") {
    return (
      <span className="inline-flex items-center gap-2 rounded-full bg-yellow-950 px-3 py-1.5 text-sm font-medium text-yellow-400">
        <Clock size={16} />
        Partial
      </span>
    );
  }

  return (
    <span className="inline-flex items-center gap-2 rounded-full bg-red-950 px-3 py-1.5 text-sm font-medium text-red-400">
      <XCircle size={16} />
      Failed
    </span>
  );
}

export default function PostDetailsPage() {
  const params = useParams();
  const token = useAuthStore((state) => state.token);

  const postId = params.id as string;

  const [post, setPost] = useState<Post | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadPost() {
      if (!token || !postId) {
        setLoading(false);
        return;
      }

      try {
        setLoading(true);
        setError("");

        const response = await api.get<Post>(
          `/posts/${postId}`,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        setPost(response.data);
      } catch (err: any) {
        console.error(err);

        setError(
          err?.response?.data?.detail ||
            "Unable to load this post."
        );
      } finally {
        setLoading(false);
      }
    }

    loadPost();
  }, [token, postId]);

  if (loading) {
    return (
      <div className="min-h-screen bg-zinc-950 p-8 text-white">
        <div className="mx-auto max-w-5xl rounded-xl border border-zinc-800 bg-zinc-900 p-12 text-center text-zinc-500">
          Loading post...
        </div>
      </div>
    );
  }

  if (error || !post) {
    return (
      <div className="min-h-screen bg-zinc-950 p-8 text-white">
        <div className="mx-auto max-w-5xl">
          <Link
            href="/posts"
            className="mb-6 inline-flex items-center gap-2 text-sm text-zinc-400 hover:text-white"
          >
            <ArrowLeft size={18} />
            Back to Posts
          </Link>

          <div className="rounded-xl border border-red-900 bg-red-950/30 p-6 text-red-300">
            {error || "Post not found."}
          </div>
        </div>
      </div>
    );
  }

  const facebookPublished = Boolean(post.facebook_post_id);
  const instagramPublished = Boolean(post.instagram_media_id);

  return (
    <div className="min-h-screen bg-zinc-950 text-white">

      {/* Header */}
      <header className="border-b border-zinc-800">
        <div className="mx-auto flex h-16 max-w-6xl items-center justify-between px-6">
          <div className="flex items-center gap-4">
            <Link
              href="/posts"
              className="rounded-lg p-2 text-zinc-400 hover:bg-zinc-800 hover:text-white"
            >
              <ArrowLeft size={20} />
            </Link>

            <div>
              <h1 className="font-semibold">
                Post Details
              </h1>

              <p className="text-xs text-zinc-500">
                View publishing information
              </p>
            </div>
          </div>

          <Link
            href="/create-post"
            className="rounded-lg bg-white px-4 py-2 text-sm font-medium text-black hover:bg-zinc-200"
          >
            Create Post
          </Link>
        </div>
      </header>

      {/* Main */}
      <main className="mx-auto max-w-6xl p-6 lg:p-8">

        <div className="grid gap-6 lg:grid-cols-[1.4fr_1fr]">

          {/* Image */}
          <section className="overflow-hidden rounded-2xl border border-zinc-800 bg-zinc-900">

            <div className="bg-zinc-950">
              <img
                src={post.image_url}
                alt="Post media"
                className="max-h-[700px] w-full object-contain"
              />
            </div>

          </section>

          {/* Details */}
          <section className="space-y-5">

            {/* Status */}
            <div className="rounded-2xl border border-zinc-800 bg-zinc-900 p-6">
              <div className="flex items-center justify-between">
                <h2 className="text-lg font-semibold">
                  Publishing Status
                </h2>

                <StatusBadge status={post.status} />
              </div>

              <div className="mt-5 space-y-2 text-sm text-zinc-500">
                <div className="flex justify-between">
                  <span>Published</span>
                  <span className="text-zinc-300">
                    {formatDate(post.published_at)}
                  </span>
                </div>

                <div className="flex justify-between">
                  <span>Created</span>
                  <span className="text-zinc-300">
                    {formatDate(post.created_at)}
                  </span>
                </div>
              </div>
            </div>

            {/* Caption */}
            <div className="rounded-2xl border border-zinc-800 bg-zinc-900 p-6">
              <h2 className="text-lg font-semibold">
                Caption
              </h2>

              <p className="mt-4 whitespace-pre-wrap text-sm leading-6 text-zinc-300">
                {post.caption}
              </p>
            </div>

            {/* Platforms */}
            <div className="rounded-2xl border border-zinc-800 bg-zinc-900 p-6">

              <h2 className="text-lg font-semibold">
                Platforms
              </h2>

              <div className="mt-5 space-y-3">

                {/* Facebook */}
                <div
                  className={`rounded-xl border p-4 ${
                    facebookPublished
                      ? "border-emerald-900 bg-emerald-950/20"
                      : "border-zinc-800 bg-zinc-950"
                  }`}
                >
                  <div className="flex items-center justify-between">

                    <div className="flex items-center gap-3">
                      <span className="text-lg font-bold">f</span>
                      <span className="font-medium">
                        Facebook
                      </span>
                    </div>

                    <span
                      className={
                        facebookPublished
                          ? "text-sm text-emerald-400"
                          : "text-sm text-zinc-500"
                      }
                    >
                      {facebookPublished
                        ? "Published"
                        : "Not published"}
                    </span>

                  </div>

                  {post.facebook_post_id && (
                    <p className="mt-3 break-all text-xs text-zinc-500">
                      Post ID: {post.facebook_post_id}
                    </p>
                  )}
                </div>

                {/* Instagram */}
                <div
                  className={`rounded-xl border p-4 ${
                    instagramPublished
                      ? "border-emerald-900 bg-emerald-950/20"
                      : "border-zinc-800 bg-zinc-950"
                  }`}
                >
                  <div className="flex items-center justify-between">

                    <div className="flex items-center gap-3">
                      <span className="text-lg font-bold">◎</span>
                      <span className="font-medium">
                        Instagram
                      </span>
                    </div>

                    <span
                      className={
                        instagramPublished
                          ? "text-sm text-emerald-400"
                          : "text-sm text-zinc-500"
                      }
                    >
                      {instagramPublished
                        ? "Published"
                        : "Not published"}
                    </span>

                  </div>

                  {post.instagram_media_id && (
                    <p className="mt-3 break-all text-xs text-zinc-500">
                      Media ID: {post.instagram_media_id}
                    </p>
                  )}
                </div>

              </div>
            </div>

            {/* Error */}
            {post.error_message && (
              <div className="rounded-2xl border border-red-900 bg-red-950/30 p-6">

                <div className="flex items-center gap-2 text-red-400">
                  <XCircle size={18} />

                  <h2 className="font-semibold">
                    Publishing Issue
                  </h2>
                </div>

                <p className="mt-3 text-sm leading-6 text-red-300/80">
                  {post.error_message}
                </p>

              </div>
            )}

          </section>
        </div>
      </main>
    </div>
  );
}