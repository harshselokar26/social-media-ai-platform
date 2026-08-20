"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import {
  ArrowLeft,
  CheckCircle2,
  Link2,
  RefreshCw,
  Unplug,
} from "lucide-react";

import { api } from "@/lib/api";
import { useAuthStore } from "@/lib/auth";

type FacebookPage = {
  id: string;
  name: string;
};

type InstagramAccount = {
  id: string;
  username?: string;
  name?: string;
  profile_picture_url?: string;
};

export default function AccountsPage() {
  const token = useAuthStore((state) => state.token);

  const [facebookPages, setFacebookPages] = useState<FacebookPage[]>([]);
  const [instagram, setInstagram] =
    useState<InstagramAccount | null>(null);

  const [facebookLoading, setFacebookLoading] = useState(true);
  const [instagramLoading, setInstagramLoading] = useState(true);

  const [facebookConnected, setFacebookConnected] = useState(false);
  const [instagramConnected, setInstagramConnected] = useState(false);

  const [facebookError, setFacebookError] = useState("");
  const [instagramError, setInstagramError] = useState("");

  async function loadFacebook() {
    if (!token) return;

    setFacebookLoading(true);
    setFacebookError("");

    try {
      const response = await api.get("/auth/meta/pages", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      const pages = response.data?.data || [];

      setFacebookPages(pages);
      setFacebookConnected(pages.length > 0);
    } catch (error: any) {
      setFacebookConnected(false);

      if (error.response?.status !== 404) {
        setFacebookError(
          error.response?.data?.detail ||
            "Unable to load Facebook connection."
        );
      }
    } finally {
      setFacebookLoading(false);
    }
  }

  async function loadInstagram() {
    if (!token) return;

    setInstagramLoading(true);
    setInstagramError("");

    try {
      const response = await api.get("/auth/instagram/account", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      setInstagram(response.data);
      setInstagramConnected(true);
    } catch (error: any) {
      setInstagramConnected(false);
      setInstagram(null);

      if (error.response?.status !== 404) {
        setInstagramError(
          error.response?.data?.detail ||
            "Unable to load Instagram connection."
        );
      }
    } finally {
      setInstagramLoading(false);
    }
  }

  async function connectFacebook() {
    try {
      const response = await api.get("/auth/meta", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      const authUrl = response.data?.auth_url;

      if (authUrl) {
        window.location.href = authUrl;
      }
    } catch (error) {
      console.error("Facebook connection failed:", error);
      setFacebookError("Unable to start Facebook connection.");
    }
  }

  async function connectInstagram() {
    try {
      const response = await api.get("/auth/instagram", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      const authUrl = response.data?.auth_url;

      if (authUrl) {
        window.location.href = authUrl;
      }
    } catch (error) {
      console.error("Instagram connection failed:", error);
      setInstagramError("Unable to start Instagram connection.");
    }
  }

  useEffect(() => {
    if (!token) return;

    loadFacebook();
    loadInstagram();
  }, [token]);

  return (
    <div className="min-h-screen bg-zinc-950 text-white">

      {/* Header */}
      <header className="border-b border-zinc-800">
        <div className="mx-auto flex h-16 max-w-6xl items-center justify-between px-6">

          <div className="flex items-center gap-4">

            <Link
              href="/dashboard"
              className="rounded-lg p-2 text-zinc-400 transition hover:bg-zinc-800 hover:text-white"
            >
              <ArrowLeft size={20} />
            </Link>

            <div>
              <h1 className="font-semibold">
                Connected Accounts
              </h1>

              <p className="text-xs text-zinc-500">
                Manage your social media connections
              </p>
            </div>

          </div>

          <Link
            href="/dashboard"
            className="text-sm text-zinc-400 hover:text-white"
          >
            Dashboard
          </Link>

        </div>
      </header>

      {/* Content */}
      <main className="mx-auto max-w-6xl space-y-6 p-6 lg:p-8">

        <section>
          <h2 className="text-2xl font-semibold">
            Social accounts
          </h2>

          <p className="mt-1 text-sm text-zinc-500">
            Connect your accounts so you can publish content directly
            from SocialAI.
          </p>
        </section>

        {/* Facebook */}
        <section className="rounded-2xl border border-zinc-800 bg-zinc-900 p-6">

          <div className="flex flex-col gap-6 md:flex-row md:items-center md:justify-between">

            <div className="flex gap-4">

              <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-zinc-800">
                <span className="text-lg font-bold">f</span>
              </div>

              <div>
                <div className="flex items-center gap-2">

                  <h3 className="font-semibold">
                    Facebook
                  </h3>

                  {facebookConnected && (
                    <span className="flex items-center gap-1 text-xs text-green-400">
                      <CheckCircle2 size={14} />
                      Connected
                    </span>
                  )}

                </div>

                <p className="mt-1 text-sm text-zinc-500">
                  Connect Facebook Pages for publishing.
                </p>

              </div>

            </div>

            <button
              onClick={connectFacebook}
              className="inline-flex items-center justify-center gap-2 rounded-lg bg-white px-4 py-2.5 text-sm font-medium text-black transition hover:bg-zinc-200"
            >
              {facebookConnected ? (
                <>
                  <RefreshCw size={16} />
                  Reconnect
                </>
              ) : (
                <>
                  <Link2 size={16} />
                  Connect Facebook
                </>
              )}
            </button>

          </div>

          {facebookLoading && (
            <div className="mt-6 flex items-center gap-2 text-sm text-zinc-500">
              <RefreshCw className="animate-spin" size={16} />
              Checking Facebook connection...
            </div>
          )}

          {facebookError && (
            <div className="mt-6 rounded-lg border border-red-900 bg-red-950/40 p-4 text-sm text-red-300">
              {facebookError}
            </div>
          )}

          {!facebookLoading && facebookConnected && (
            <div className="mt-6 space-y-3">

              <p className="text-xs font-medium uppercase tracking-wide text-zinc-500">
                Connected Pages
              </p>

              {facebookPages.map((page) => (
                <div
                  key={page.id}
                  className="flex items-center justify-between rounded-xl border border-zinc-800 bg-zinc-950 p-4"
                >
                  <div>
                    <p className="font-medium">
                      {page.name}
                    </p>

                    <p className="mt-1 text-xs text-zinc-600">
                      Page ID: {page.id}
                    </p>
                  </div>

                  <CheckCircle2
                    size={20}
                    className="text-green-400"
                  />
                </div>
              ))}

            </div>
          )}

          {!facebookLoading && !facebookConnected && !facebookError && (
            <div className="mt-6 rounded-xl border border-dashed border-zinc-800 p-6 text-center">
              <Unplug
                className="mx-auto text-zinc-600"
                size={28}
              />

              <p className="mt-3 text-sm text-zinc-400">
                No Facebook Pages connected.
              </p>

              <p className="mt-1 text-xs text-zinc-600">
                Connect Facebook to see your available Pages.
              </p>
            </div>
          )}

        </section>

        {/* Instagram */}
        <section className="rounded-2xl border border-zinc-800 bg-zinc-900 p-6">

          <div className="flex flex-col gap-6 md:flex-row md:items-center md:justify-between">

            <div className="flex gap-4">

              <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-zinc-800">
                <span className="text-lg font-bold">◎</span>
              </div>

              <div>
                <div className="flex items-center gap-2">

                  <h3 className="font-semibold">
                    Instagram
                  </h3>

                  {instagramConnected && (
                    <span className="flex items-center gap-1 text-xs text-green-400">
                      <CheckCircle2 size={14} />
                      Connected
                    </span>
                  )}

                </div>

                <p className="mt-1 text-sm text-zinc-500">
                  Connect an Instagram account for publishing.
                </p>

              </div>

            </div>

            <button
              onClick={connectInstagram}
              className="inline-flex items-center justify-center gap-2 rounded-lg bg-white px-4 py-2.5 text-sm font-medium text-black transition hover:bg-zinc-200"
            >
              {instagramConnected ? (
                <>
                  <RefreshCw size={16} />
                  Reconnect
                </>
              ) : (
                <>
                  <Link2 size={16} />
                  Connect Instagram
                </>
              )}
            </button>

          </div>

          {instagramLoading && (
            <div className="mt-6 flex items-center gap-2 text-sm text-zinc-500">
              <RefreshCw className="animate-spin" size={16} />
              Checking Instagram connection...
            </div>
          )}

          {instagramError && (
            <div className="mt-6 rounded-lg border border-red-900 bg-red-950/40 p-4 text-sm text-red-300">
              {instagramError}
            </div>
          )}

          {!instagramLoading && instagramConnected && instagram && (
            <div className="mt-6 rounded-xl border border-zinc-800 bg-zinc-950 p-4">

              <div className="flex items-center gap-4">

                {instagram.profile_picture_url ? (
                  <img
                    src={instagram.profile_picture_url}
                    alt={instagram.username || "Instagram"}
                    className="h-12 w-12 rounded-full object-cover"
                  />
                ) : (
                  <div className="flex h-12 w-12 items-center justify-center rounded-full bg-zinc-800">
                    <span className="text-lg font-bold">◎</span>
                  </div>
                )}

                <div>
                  <p className="font-medium">
                    {instagram.username
                      ? `@${instagram.username}`
                      : instagram.name || "Instagram account"}
                  </p>

                  {instagram.name && instagram.username && (
                    <p className="mt-1 text-sm text-zinc-500">
                      {instagram.name}
                    </p>
                  )}

                  <p className="mt-1 text-xs text-zinc-600">
                    Account ID: {instagram.id}
                  </p>
                </div>

                <CheckCircle2
                  className="ml-auto text-green-400"
                  size={20}
                />

              </div>

            </div>
          )}

          {!instagramLoading &&
            !instagramConnected &&
            !instagramError && (
              <div className="mt-6 rounded-xl border border-dashed border-zinc-800 p-6 text-center">

                <Unplug
                  className="mx-auto text-zinc-600"
                  size={28}
                />

                <p className="mt-3 text-sm text-zinc-400">
                  No Instagram account connected.
                </p>

                <p className="mt-1 text-xs text-zinc-600">
                  Connect Instagram to enable publishing.
                </p>

              </div>
            )}

        </section>

      </main>
    </div>
  );
}