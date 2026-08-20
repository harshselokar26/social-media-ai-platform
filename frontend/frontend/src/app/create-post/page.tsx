"use client";

import { ChangeEvent, useMemo, useState } from "react";
import Link from "next/link";
import {
  ArrowLeft,
  CheckCircle2,
  ImagePlus,
  Loader2,
  Send,
  CalendarClock,
} from "lucide-react";

import { api } from "@/lib/api";
import { useAuthStore } from "@/lib/auth";

type PublishMode = "now" | "schedule";

export default function CreatePostPage() {
  const token = useAuthStore((state) => state.token);

  const [caption, setCaption] = useState("");
  const [hashtags, setHashtags] = useState<string[]>([]);
  const [aiTopic, setAiTopic] = useState("");
  const [aiPlatform, setAiPlatform] = useState("instagram");
  const [aiTone, setAiTone] = useState("professional");
  const [generatingCaption, setGeneratingCaption] = useState(false);

  const [platforms, setPlatforms] = useState<string[]>([
    "facebook",
    "instagram",
  ]);

  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState("");

  const [publishMode, setPublishMode] =
    useState<PublishMode>("now");

  const [scheduledDate, setScheduledDate] = useState("");
  const [scheduledTime, setScheduledTime] = useState("");

  const [uploading, setUploading] = useState(false);
  const [publishing, setPublishing] = useState(false);

  const [success, setSuccess] = useState("");
  const [error, setError] = useState("");

  function formatDateForInput(date: Date) {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, "0");
    const day = String(date.getDate()).padStart(2, "0");

    return `${year}-${month}-${day}`;
  }

  function formatDateLabel(dateString: string) {
    const date = new Date(`${dateString}T00:00:00`);

    return date.toLocaleDateString("en-IN", {
      weekday: "long",
      day: "numeric",
      month: "short",
      year: "numeric",
    });
  }

  function formatTimeLabel(time: string) {
    const [hours, minutes] = time.split(":").map(Number);
    const date = new Date();
    date.setHours(hours, minutes, 0, 0);

    return date.toLocaleTimeString("en-IN", {
      hour: "numeric",
      minute: "2-digit",
      hour12: true,
    });
  }

  const availableDates = useMemo(() => {
    const dates: string[] = [];
    const today = new Date();

    for (let i = 0; i < 30; i += 1) {
      const date = new Date(today);
      date.setDate(today.getDate() + i);
      dates.push(formatDateForInput(date));
    }

    return dates;
  }, []);

  const availableTimes = useMemo(() => {
    const times: string[] = [];

    for (let hour = 0; hour < 24; hour += 1) {
      for (let minute = 0; minute < 60; minute += 15) {
        times.push(
          `${String(hour).padStart(2, "0")}:${String(minute).padStart(2, "0")}`
        );
      }
    }

    return times;
  }, []);

  function getScheduledDateTime() {
    if (!scheduledDate || !scheduledTime) {
      return null;
    }

    return new Date(`${scheduledDate}T${scheduledTime}:00`);
  }

  function togglePlatform(platform: string) {
    setPlatforms((current) =>
      current.includes(platform)
        ? current.filter((item) => item !== platform)
        : [...current, platform]
    );
  }

  function handleFileChange(
    event: ChangeEvent<HTMLInputElement>
  ) {
    const selected = event.target.files?.[0];

    if (!selected) return;

    setError("");
    setSuccess("");

    const allowedTypes = [
      "image/jpeg",
      "image/png",
      "image/webp",
    ];

    if (!allowedTypes.includes(selected.type)) {
      setError(
        "Please select a JPG, PNG, or WEBP image."
      );
      event.target.value = "";
      return;
    }

    const maxSize = 10 * 1024 * 1024;

    if (selected.size > maxSize) {
      setError("Image must be smaller than 10 MB.");
      event.target.value = "";
      return;
    }

    const image = new Image();

    image.onload = () => {
      const width = image.width;
      const height = image.height;

      if (width === 0 || height === 0) {
        setError("Could not read image dimensions.");
        return;
      }

      const aspectRatio = width / height;

      if (
        platforms.includes("instagram") &&
        (aspectRatio < 0.8 || aspectRatio > 1.91)
      ) {
        setError(
          `Instagram does not support this aspect ratio (${aspectRatio.toFixed(
            2
          )}:1). Use an image between 4:5 and 1.91:1.`
        );

        event.target.value = "";
        return;
      }

      setFile(selected);
      setPreview(URL.createObjectURL(selected));
    };

    image.onerror = () => {
      setError("Unable to read this image.");
      event.target.value = "";
    };

    image.src = URL.createObjectURL(selected);
  }

  async function validateInstagramImage() {
    if (!platforms.includes("instagram") || !file) {
      return true;
    }

    const image = new Image();
    const imageUrl = URL.createObjectURL(file);

    return new Promise<boolean>((resolve) => {
      image.onload = () => {
        const aspectRatio = image.width / image.height;

        URL.revokeObjectURL(imageUrl);

        resolve(
          aspectRatio >= 0.8 &&
            aspectRatio <= 1.91
        );
      };

      image.onerror = () => {
        URL.revokeObjectURL(imageUrl);
        resolve(false);
      };

      image.src = imageUrl;
    });
  }

  async function handleGenerateCaption() {
    setError("");
    setSuccess("");

    if (!token) {
      setError("You are not authenticated.");
      return;
    }

    if (!aiTopic.trim()) {
      setError("Enter a topic for AI caption generation.");
      return;
    }

    try {
      setGeneratingCaption(true);

      const response = await api.post(
        "/ai/generate-caption",
        {
          topic: aiTopic.trim(),
          platform: aiPlatform,
          tone: aiTone,
        },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      const generatedCaption = response.data?.caption;
      const generatedHashtags = response.data?.hashtags;

      if (!generatedCaption) {
        throw new Error(
          "AI did not return a caption."
        );
      }

      setCaption(generatedCaption);

      setHashtags(
        Array.isArray(generatedHashtags)
          ? generatedHashtags
          : []
      );
      setSuccess("AI caption generated successfully.");
    } catch (err: any) {
      setError(
        err.response?.data?.detail ||
          err.message ||
          "Failed to generate AI caption."
      );
    } finally {
      setGeneratingCaption(false);
    }
  }

  async function handleSubmit() {
    setError("");
    setSuccess("");

    if (!token) {
      setError("You are not authenticated.");
      return;
    }

    if (!caption.trim()) {
      setError("Please enter a caption.");
      return;
    }

    if (!file) {
      setError("Please select an image.");
      return;
    }

    if (platforms.length === 0) {
      setError("Select at least one platform.");
      return;
    }

    const finalCaption =
      hashtags.length > 0
        ? `${caption.trim()}\n\n${hashtags.join(" ")}`
        : caption.trim();

    if (publishMode === "schedule") {
      if (!scheduledDate) {
        setError("Please select a date.");
        return;
      }

      if (!scheduledTime) {
        setError("Please select a time.");
        return;
      }

      const selectedDate = getScheduledDateTime();

      if (!selectedDate || Number.isNaN(selectedDate.getTime())) {
        setError("Please select a valid date and time.");
        return;
      }

      if (selectedDate <= new Date()) {
        setError(
          "Scheduled time must be in the future."
        );
        return;
      }
    }

    const validInstagramImage =
      await validateInstagramImage();

    if (!validInstagramImage) {
      setError(
        "This image cannot be published to Instagram. Use an aspect ratio between 4:5 and 1.91:1."
      );
      return;
    }

    try {
      // ==========================================
      // 1. UPLOAD IMAGE
      // ==========================================

      setUploading(true);

      const formData = new FormData();
      formData.append("file", file);

      const uploadResponse = await api.post(
        "/media/upload",
        formData,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      const imageUrl =
        uploadResponse.data?.data?.secure_url;

      if (!imageUrl) {
        throw new Error(
          "Image upload did not return a URL."
        );
      }

      setUploading(false);

      // ==========================================
      // 2. PUBLISH NOW
      // ==========================================

      if (publishMode === "now") {
        setPublishing(true);

        const publishResponse = await api.post(
          "/posts/publish",
          {
            caption: finalCaption,
            image_url: imageUrl,
            platforms,
          },
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        const status =
          publishResponse.data?.status;

        if (status === "published") {
          setSuccess(
            "Post published successfully."
          );
        } else if (status === "partial") {
          setSuccess(
            "Post published to some platforms."
          );
        } else {
          setError(
            "Publishing failed. Check the connected accounts and try again."
          );
        }

        return;
      }

      // ==========================================
      // 3. SCHEDULE POST
      // ==========================================

      setPublishing(true);

      const scheduleResponse = await api.post(
        "/posts/schedule",
        {
          caption: finalCaption,
          image_url: imageUrl,
          platforms,
          scheduled_at: getScheduledDateTime()!.toISOString(),
        },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      const scheduledPost =
        scheduleResponse.data;

      if (scheduledPost?.status === "scheduled") {
        const selectedDateTime = getScheduledDateTime();
        const formattedDate = selectedDateTime?.toLocaleString(
          "en-IN",
          {
            dateStyle: "medium",
            timeStyle: "short",
          }
        );

        setSuccess(
          `Post scheduled successfully for ${formattedDate}.`
        );
      } else {
        setError(
          "Post could not be scheduled."
        );
      }
    } catch (err: any) {
      setError(
        err.response?.data?.detail ||
          err.message ||
          "Something went wrong."
      );
    } finally {
      setUploading(false);
      setPublishing(false);
    }
  }

  return (
    <div className="min-h-screen bg-zinc-950 text-white">
      {/* HEADER */}
      <header className="border-b border-zinc-800">
        <div className="mx-auto flex h-16 max-w-6xl items-center justify-between px-6">
          <div className="flex items-center gap-4">
            <Link
              href="/dashboard"
              className="rounded-lg p-2 text-zinc-400 hover:bg-zinc-800 hover:text-white"
            >
              <ArrowLeft size={20} />
            </Link>

            <div>
              <h1 className="font-semibold">
                Create Post
              </h1>

              <p className="text-xs text-zinc-500">
                Publish or schedule to your connected
                social accounts
              </p>
            </div>
          </div>

          <Link
            href="/accounts"
            className="text-sm text-zinc-400 hover:text-white"
          >
            Connected Accounts
          </Link>
        </div>
      </header>

      {/* MAIN */}
      <main className="mx-auto max-w-6xl p-6 lg:p-8">
        <div className="grid gap-6 lg:grid-cols-[1.5fr_1fr]">

          {/* ============================= */}
          {/* POST CONTENT */}
          {/* ============================= */}

          <section className="rounded-2xl border border-zinc-800 bg-zinc-900 p-6">
            <h2 className="text-lg font-semibold">
              Post content
            </h2>

            <div className="mt-6 space-y-6">

              {/* CAPTION */}
              <div>
                <label className="text-sm font-medium">
                  Caption
                </label>

                <textarea
                  value={caption}
                  onChange={(event) =>
                    setCaption(event.target.value)
                  }
                  rows={7}
                  placeholder="Write your caption..."
                  className="mt-2 w-full resize-none rounded-xl border border-zinc-800 bg-zinc-950 p-4 text-sm outline-none focus:border-zinc-600"
                />

                <p className="mt-2 text-xs text-zinc-600">
                  {caption.length} characters
                </p>

                <div className="mt-5 rounded-xl border border-zinc-800 bg-zinc-950 p-4">
                  <div>
                    <label className="text-xs font-medium text-zinc-400">
                      Topic
                    </label>

                    <input
                      type="text"
                      value={aiTopic}
                      onChange={(event) =>
                        setAiTopic(event.target.value)
                      }
                      placeholder="What should the caption be about?"
                      className="mt-2 w-full rounded-xl border border-zinc-800 bg-zinc-900 p-3 text-sm text-white outline-none focus:border-zinc-600"
                    />
                  </div>

                  <div className="mt-4">
                    <label className="text-xs font-medium text-zinc-400">
                      Platform
                    </label>

                    <select
                      value={aiPlatform}
                      onChange={(event) =>
                        setAiPlatform(event.target.value)
                      }
                      className="mt-2 w-full rounded-xl border border-zinc-800 bg-zinc-900 p-3 text-sm text-white outline-none focus:border-zinc-600"
                    >
                      <option value="instagram">Instagram</option>
                      <option value="facebook">Facebook</option>
                    </select>
                  </div>

                  <div className="mt-4">
                    <label className="text-xs font-medium text-zinc-400">
                      Tone
                    </label>

                    <select
                      value={aiTone}
                      onChange={(event) =>
                        setAiTone(event.target.value)
                      }
                      className="mt-2 w-full rounded-xl border border-zinc-800 bg-zinc-900 p-3 text-sm text-white outline-none focus:border-zinc-600"
                    >
                      <option value="professional">Professional</option>
                      <option value="casual">Casual</option>
                      <option value="friendly">Friendly</option>
                      <option value="funny">Funny</option>
                      <option value="inspirational">Inspirational</option>
                      <option value="promotional">Promotional</option>
                    </select>
                  </div>

                  <button
                    type="button"
                    onClick={handleGenerateCaption}
                    disabled={generatingCaption}
                    className="mt-4 flex w-full items-center justify-center gap-2 rounded-xl border border-zinc-700 bg-zinc-900 px-4 py-3 text-sm font-medium text-white hover:bg-zinc-800 disabled:cursor-not-allowed disabled:opacity-60"
                  >
                    {generatingCaption ? (
                      <>
                        <Loader2
                          size={16}
                          className="animate-spin"
                        />
                        Generating...
                      </>
                    ) : (
                      <>✨ Generate Caption</>
                    )}
                  </button>
                </div>

                {hashtags.length > 0 && (
                  <div className="mt-4 rounded-xl border border-zinc-800 bg-zinc-950 p-4">
                    <div className="mb-3">
                      <h3 className="text-sm font-semibold text-white">
                        AI Generated Hashtags
                      </h3>
                      <p className="mt-1 text-xs text-zinc-500">
                        Remove any hashtags you don't want to use.
                      </p>
                    </div>
                    <div className="flex flex-wrap gap-2">
                      {hashtags.map((hashtag, index) => (
                        <button
                          key={`${hashtag}-${index}`}
                          type="button"
                          onClick={() => {
                            setHashtags((current) =>
                              current.filter(
                                (_, hashtagIndex) =>
                                  hashtagIndex !== index
                              )
                            );
                          }}
                          className="rounded-full border border-zinc-700 bg-zinc-900 px-3 py-1.5 text-xs text-zinc-200 hover:border-red-500 hover:text-red-400"
                          title="Remove hashtag"
                        >
                          {hashtag} ×
                        </button>
                      ))}
                    </div>
                  </div>
                )}
              </div>

              {/* IMAGE */}
              <div>
                <label className="text-sm font-medium">
                  Image
                </label>

                <label className="mt-2 flex cursor-pointer flex-col items-center justify-center rounded-xl border border-dashed border-zinc-700 bg-zinc-950 p-8 text-center hover:border-zinc-500">
                  <ImagePlus
                    size={32}
                    className="text-zinc-500"
                  />

                  <p className="mt-3 text-sm text-zinc-400">
                    Click to choose an image
                  </p>

                  <p className="mt-1 text-xs text-zinc-600">
                    JPG, PNG, WEBP · Max 10 MB
                  </p>

                  <input
                    type="file"
                    accept="image/jpeg,image/png,image/webp"
                    onChange={handleFileChange}
                    className="hidden"
                  />
                </label>

                {preview && (
                  <img
                    src={preview}
                    alt="Preview"
                    className="mt-4 max-h-96 w-full rounded-xl border border-zinc-800 object-cover"
                  />
                )}
              </div>
            </div>
          </section>

          {/* ============================= */}
          {/* PUBLISH PANEL */}
          {/* ============================= */}

          <section className="rounded-2xl border border-zinc-800 bg-zinc-900 p-6">
            <h2 className="text-lg font-semibold">
              Publish
            </h2>

            {/* MODE */}
            <div className="mt-6">
              <label className="text-sm font-medium">
                Publishing mode
              </label>

              <div className="mt-3 grid grid-cols-2 gap-3">

                {/* NOW */}
                <button
                  type="button"
                  onClick={() =>
                    setPublishMode("now")
                  }
                  className={`rounded-xl border p-4 text-left ${
                    publishMode === "now"
                      ? "border-green-700 bg-green-950/30"
                      : "border-zinc-800 bg-zinc-950"
                  }`}
                >
                  <div className="flex items-center gap-2">
                    <Send size={18} />

                    <span className="font-medium">
                      Publish Now
                    </span>
                  </div>

                  <p className="mt-1 text-xs text-zinc-500">
                    Publish immediately
                  </p>
                </button>

                {/* SCHEDULE */}
                <button
                  type="button"
                  onClick={() =>
                    setPublishMode("schedule")
                  }
                  className={`rounded-xl border p-4 text-left ${
                    publishMode === "schedule"
                      ? "border-green-700 bg-green-950/30"
                      : "border-zinc-800 bg-zinc-950"
                  }`}
                >
                  <div className="flex items-center gap-2">
                    <CalendarClock size={18} />

                    <span className="font-medium">
                      Schedule
                    </span>
                  </div>

                  <p className="mt-1 text-xs text-zinc-500">
                    Publish at a specific time
                  </p>
                </button>
              </div>
            </div>

            {/* SCHEDULE DATE */}
            {publishMode === "schedule" && (
              <div className="mt-6 space-y-4">
                <div>
                  <label className="text-sm font-medium">
                    Schedule date
                  </label>

                  <select
                    value={scheduledDate}
                    onChange={(event) => {
                      setScheduledDate(event.target.value);
                      setScheduledTime("");
                      setError("");
                    }}
                    className="mt-2 w-full rounded-xl border border-zinc-800 bg-zinc-950 p-4 text-sm text-white outline-none focus:border-zinc-600"
                  >
                    <option value="">Select a date</option>
                    {availableDates.map((date) => (
                      <option key={date} value={date}>
                        {formatDateLabel(date)}
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="text-sm font-medium">
                    Schedule time
                  </label>

                  <select
                    value={scheduledTime}
                    onChange={(event) => {
                      setScheduledTime(event.target.value);
                      setError("");
                    }}
                    disabled={!scheduledDate}
                    className="mt-2 w-full rounded-xl border border-zinc-800 bg-zinc-950 p-4 text-sm text-white outline-none focus:border-zinc-600 disabled:cursor-not-allowed disabled:opacity-50"
                  >
                    <option value="">
                      {scheduledDate
                        ? "Select a time"
                        : "Select a date first"}
                    </option>
                    {availableTimes
                      .filter((time) => {
                        const selectedDate = scheduledDate
                          ? new Date(`${scheduledDate}T${time}:00`)
                          : null;

                        return selectedDate !== null && selectedDate > new Date();
                      })
                      .map((time) => (
                        <option key={time} value={time}>
                          {formatTimeLabel(time)}
                        </option>
                      ))}
                  </select>
                </div>

                <p className="text-xs text-zinc-600">
                  Select a future date and time.
                </p>
              </div>
            )}

            {/* PLATFORMS */}
            <div className="mt-6">
              <label className="text-sm font-medium">
                Platforms
              </label>

              <div className="mt-3 space-y-3">

                {/* FACEBOOK */}
                <button
                  type="button"
                  onClick={() =>
                    togglePlatform("facebook")
                  }
                  className={`flex w-full items-center justify-between rounded-xl border p-4 text-left ${
                    platforms.includes("facebook")
                      ? "border-green-700 bg-green-950/30"
                      : "border-zinc-800 bg-zinc-950"
                  }`}
                >
                  <div className="flex items-center gap-3">
                    <span className="text-lg font-bold">
                      f
                    </span>

                    <span>Facebook</span>
                  </div>

                  {platforms.includes("facebook") && (
                    <CheckCircle2
                      size={20}
                      className="text-green-400"
                    />
                  )}
                </button>

                {/* INSTAGRAM */}
                <button
                  type="button"
                  onClick={() =>
                    togglePlatform("instagram")
                  }
                  className={`flex w-full items-center justify-between rounded-xl border p-4 text-left ${
                    platforms.includes("instagram")
                      ? "border-green-700 bg-green-950/30"
                      : "border-zinc-800 bg-zinc-950"
                  }`}
                >
                  <div className="flex items-center gap-3">
                    <span className="text-lg font-bold">
                      ◎
                    </span>

                    <span>Instagram</span>
                  </div>

                  {platforms.includes("instagram") && (
                    <CheckCircle2
                      size={20}
                      className="text-green-400"
                    />
                  )}
                </button>
              </div>
            </div>

            {/* ERROR */}
            {error && (
              <div className="mt-6 rounded-xl border border-red-900 bg-red-950/40 p-4 text-sm text-red-300">
                {error}
              </div>
            )}

            {/* SUCCESS */}
            {success && (
              <div className="mt-6 rounded-xl border border-green-900 bg-green-950/40 p-4 text-sm text-green-300">
                {success}
              </div>
            )}

            {/* SUBMIT */}
            <button
              type="button"
              onClick={handleSubmit}
              disabled={
                uploading || publishing
              }
              className="mt-6 flex w-full items-center justify-center gap-2 rounded-xl bg-white px-5 py-3 font-medium text-black hover:bg-zinc-200 disabled:cursor-not-allowed disabled:opacity-60"
            >
              {uploading || publishing ? (
                <>
                  <Loader2
                    size={18}
                    className="animate-spin"
                  />

                  {uploading
                    ? "Uploading..."
                    : publishMode === "schedule"
                    ? "Scheduling..."
                    : "Publishing..."}
                </>
              ) : publishMode === "schedule" ? (
                <>
                  <CalendarClock size={18} />
                  Schedule Post
                </>
              ) : (
                <>
                  <Send size={18} />
                  Publish Post
                </>
              )}
            </button>

            <p className="mt-3 text-center text-xs text-zinc-600">
              The image is uploaded to Cloudinary before
              publishing or scheduling.
            </p>
          </section>
        </div>
      </main>
    </div>
  );
}