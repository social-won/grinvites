import React, { createContext, useContext, useEffect, useState } from "react";
import { getUser } from "@/lib/api";
import supabase from "@/lib/supabase";
import { AuthChangeEvent, Session } from "@supabase/supabase-js";
import { GrinvitesUser } from "@/lib/types";
import { useTheme, Theme } from "./theme-context";

interface UserContextType {
  user: GrinvitesUser | null;
  loading: boolean;
  error: Error | null;
  // refetch: () => Promise<void>;
  setUser: React.Dispatch<React.SetStateAction<GrinvitesUser | null>>;
}

const UserContext = createContext<UserContextType | undefined>(undefined);

export function UserProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<GrinvitesUser | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);
  const { setTheme } = useTheme();

  const handleAuthChange = async (_e: AuthChangeEvent, session: Session | null) => {
    console.log("auth changed!", session, _e);

    
    if (!session?.user) {
      setUser(null);
      setLoading(false);
      return;
    }

    try {
      setLoading(true);
      setError(null);

      const data = await getUser(session.user.id, session.access_token).catch((e) => {
        console.log("ERROR!")
        console.log(e)
      });

      if (!data?.data) {
        // On SIGNED_IN, a 404 means signup is in progress — the signup page
        // will call setUser directly once createUser completes.
        if (_e !== "SIGNED_IN") setError(new Error("User not found in database"))
        return;
      }

      setUser(data.data);
      if (data.data?.theme) setTheme(data.data.theme as Theme);
    } catch (err) {
      const error = err instanceof Error ? err : new Error("Unknown error");
      setError(error);
      setUser(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    console.log("user updated!", user);
    
  }, [user])
  

  useEffect(() => {
    console.log("Set up auth change listener")
    const { data: listener } = supabase.auth.onAuthStateChange(handleAuthChange);

    return () => {
      listener?.subscription?.unsubscribe();
    };
  }, []);

  return (
    <UserContext.Provider value={{ user, loading, error, setUser }}>
      {children}
    </UserContext.Provider>
  );
}

export function useUser() {
  const context = useContext(UserContext);
  if (context === undefined) {
    throw new Error("useUser must be used within a UserProvider");
  }
  return context;
}
